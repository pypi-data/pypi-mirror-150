
from twisted.internet.defer import succeed

from ebs.linuxnode.modapi.engine import ModularHttpApiEngine


class MultiWebApiCoreEngine(ModularHttpApiEngine):
    _prefix = "multiweb"
    _api_probe = 'api_test_connection'
    _api_tasks = []
    _api_reconnect_frequency = 30
    _api_baseurl = 'config:multiweb_api_url'
    _api_headers = {'Content-Type': 'application/json',
                    'Accept': 'application/json'}
    _api_language = 'json'
    _api_ep_test_connection = 'applications'

    @property
    def api_token(self):
        return succeed(None)

    def api_token_reset(self):
        return succeed(None)

    def _api_basic_params(self, token):
        return {
            '_method': 'GET',
            '_language': self._api_language
        }

    def _api_test_query_params(self, token):
        rv = self._api_basic_params(token)
        return rv

    def _api_ep_test_connection_handler(self, response):
        return succeed(True)

    def api_test_connection(self):
        return self._api_execute(
            self._api_ep_test_connection,
            self._api_test_query_params,
            self._api_ep_test_connection_handler
        )
