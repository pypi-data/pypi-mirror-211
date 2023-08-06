import logging
import os
import signal
from threading import Event, Thread
from time import sleep
from typing import Optional

import schedule
from requests.exceptions import RequestException
from requests_cache import CachedSession

from sentry_dynamic_sampling_lib.shared import AppConfig, Metric, MetricType
from sentry_dynamic_sampling_lib.utils import Singleton

try:
    from celery.signals import worker_shutdown
except ModuleNotFoundError:
    worker_shutdown = None  # pylint: disable=invalid-name

LOGGER = logging.getLogger("SentryWrapper")


def on_exit(*args, **kwargs):  # pylint: disable=unused-argument
    trace_sampler = TraceSampler()
    trace_sampler.kill()
    LOGGER.debug("ControllerClient Killed")
    raise KeyboardInterrupt


# pylint: disable=too-many-instance-attributes
class ControllerClient(Thread):
    def __init__(
        self,
        *args,
        poll_interval=None,
        metric_interval=None,
        controller_endpoint=None,
        metric_endpoint=None,
        app_key=None,
        **kwargs
    ) -> None:
        self.poll_interval = poll_interval
        self.metric_interval = metric_interval
        self.controller_endpoint = controller_endpoint
        self.metric_endpoint = metric_endpoint
        self.app_key = app_key

        self.__stopper = Event()
        self.app_config = AppConfig()
        self.metrics = Metric()
        self.session = CachedSession(backend="memory", cache_control=True)

        LOGGER.debug("ControllerClient Initialized")
        super().__init__(*args, name="SentryControllerClient", **kwargs)

    def run(self):
        # HACK: Django change the timezone mid startup
        # Which break the datetime.datetime.now() method
        # This then break schedule by delaying the startup by the timezone delta
        sleep(5)
        schedule.every(self.poll_interval).seconds.do(self.update_config)
        schedule.every(self.metric_interval).seconds.do(self.update_metrics)
        LOGGER.debug("ControllerClient Started")
        while not self.__stopper.is_set():
            schedule.run_pending()
            sleep(1)

    def kill(self):
        self.__stopper.set()
        if self.is_alive():
            self.join()

    def update_config(self):
        try:
            resp = self.session.get(self.controller_endpoint.format(self.app_key), timeout=1)
            resp.raise_for_status()
        except RequestException as err:
            LOGGER.warning("App Request Failed: %s", err)
            return

        if resp.from_cache:
            LOGGER.debug("Config Polled from cache")
            return

        LOGGER.debug("Config Polled")
        data = resp.json()
        self.app_config.update(data)
        self.metrics.set_mode(MetricType.CELERY, data["celery_collect_metrics"])
        self.metrics.set_mode(MetricType.WSGI, data["wsgi_collect_metrics"])

    def update_metrics(self):
        for metric_type, data in self.metrics:
            data = {
                "app": self.app_key,
                "type": metric_type.value,
                "data": dict(data),
            }
            try:
                self.session.post(
                    self.metric_endpoint.format(self.app_key, metric_type.value),
                    json=data,
                )
                LOGGER.debug("Metric %s pushed", metric_type.value)
            except RequestException as err:
                LOGGER.warning("Metric Request Failed: %s", err)
                continue


class TraceSampler(metaclass=Singleton):
    def __init__(self, *args, **kwargs) -> None:
        self.params = (args, kwargs)
        self._controller: Optional[ControllerClient] = None
        self._tread_for_pid: Optional[int] = None

        signal.signal(signal.SIGINT, on_exit)
        # HACK: Celery has a built in signal mechanism
        # so we use it
        if worker_shutdown:
            worker_shutdown.connect(on_exit)

    @property
    def has_running_controller(self):
        if self._tread_for_pid != os.getpid() or not self._controller:
            return False
        return self._controller.is_alive()

    @property
    def app_config(self) -> AppConfig:
        return self._controller.app_config

    @property
    def metrics(self) -> Metric:
        return self._controller.metrics

    def kill(self):
        if self._controller:
            self._controller.kill()

    def _start_controller(self):
        args, kwargs = self.params
        self._controller = ControllerClient(*args, **kwargs)
        self._controller.start()
        self._tread_for_pid = os.getpid()

    def _ensure_controller(self):
        if not self.has_running_controller:
            self._start_controller()

    def __del__(self):
        self.kill()

    def __call__(self, sampling_context):
        self._ensure_controller()
        if sampling_context:
            if "wsgi_environ" in sampling_context:
                path = sampling_context["wsgi_environ"].get("PATH_INFO", "")
                user_agent = sampling_context["wsgi_environ"].get("HTTP_USER_AGENT", "")
                if path in self.app_config.ignored_paths or user_agent.startswith(self.app_config.ignored_user_agents):
                    return 0
                self.metrics.count_path(path)
                self.metrics.count_user_agent(user_agent)
            if "celery_job" in sampling_context:
                task = sampling_context["celery_job"].get("task", "")
                if task in self.app_config.ignored_tasks:
                    return 0
                self.metrics.count_task(task)
        return self.app_config.sample_rate
