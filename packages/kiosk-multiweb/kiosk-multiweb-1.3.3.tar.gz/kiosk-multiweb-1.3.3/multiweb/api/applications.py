

from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from .core import MultiWebApiCoreEngine


class MultiWebApplicationsEngine(MultiWebApiCoreEngine):
    _api_ep_applications = 'applications'

    def __init__(self, *args, **kwargs):
        super(MultiWebApplicationsEngine, self).__init__(*args, **kwargs)
        self._retries = 0
        self._rapid_checks = 0
        self._api_applications_task = None

    def _api_applications_handler(self, response):
        response = response['data']
        self.log.info("Got Applications API Response with {n} Entries",
                      n=len(response))
        if len(response):
            self._retries = 0
            self._rapid_checks = 0
            self._actual.multiweb_applications_update(response)
        else:
            self._retries += 1
            if self._retries >= 3:
                self._rapid_checks += 1
                if self._rapid_checks < 10:
                    reactor.callLater(60, self.api_get_applications)
                self._actual.multiweb_applications_update(response)
            else:
                self.api_get_applications()

    def _api_application_params(self, token):
        rv = self._api_basic_params(token)
        return rv

    def api_get_applications(self):
        return self._api_execute(
            self._api_ep_applications,
            self._api_application_params,
            self._api_applications_handler
        )

    """ Applications API Management Task """
    @property
    def api_applications_task(self):
        if self._api_applications_task is None:
            self._api_applications_task = LoopingCall(self.api_get_applications)
        return self._api_applications_task
