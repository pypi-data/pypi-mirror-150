

import arrow
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from multiweb import api
from ebs.linuxnode.modapi.standalone import StandaloneActual
from ebs.linuxnode.modapi.standalone import StandaloneConfig


class StandaloneActualMultiWeb(StandaloneActual):
    def multiweb_applications_update(self, response):
        nitems = len(response)
        print(arrow.now(), nitems)
        for item in response:
            print("{:15} {}".format(item['name'], item['link']))


class StandaloneConfigMultiWeb(StandaloneConfig):
    def __init__(self, *args, **kwargs):
        super(StandaloneConfigMultiWeb, self).__init__(*args, **kwargs)
        self.multiweb_api_url = 'https://apps.starxmedia.in/api/v1'


config = StandaloneConfigMultiWeb()
e = api.MultiWebApiEngine(StandaloneActualMultiWeb(), config=config)


def get_results_summary():
    e.api_get_applications()


if __name__ == '__main__':
    period = 10
    print("API Response Test:")
    print(" API Url : {}".format(config.multiweb_api_url))
    print(" Period: {}s".format(period))
    loop = LoopingCall(get_results_summary)
    loopDeferred = loop.start(period)
    reactor.run()
