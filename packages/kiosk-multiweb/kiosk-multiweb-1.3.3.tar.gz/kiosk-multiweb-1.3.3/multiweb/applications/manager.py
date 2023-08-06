

import os
from urllib.parse import urlparse
from twisted import logger
from twisted.internet.defer import inlineCallbacks

from ebs.linuxnode.core.constants import ASSET


class MultiWebApplication(object):
    def __init__(self, parent, spec):
        self._parent = parent
        self._spec = spec

    @property
    def parent(self):
        return self._parent

    @property
    def actual(self):
        return self.parent.actual

    @property
    def id(self):
        return self._spec['id']

    @property
    def name(self):
        return self._spec['name']

    @property
    def description(self):
        return self._spec['description'] or ''

    @property
    def url(self):
        return self._spec['link']

    @property
    def whitelist_urls(self):
        return self._spec['whitelist_urls']

    @property
    def blacklist_urls(self):
        return self._spec['blacklist_urls']

    @property
    def avatar_url(self):
        return self._spec['avatar']['large']

    @property
    def avatar_filename(self):
        return os.path.basename(urlparse(self.avatar_url).path)

    @property
    def avatar(self):
        return self.actual.resource_manager.get(self.avatar_filename).filepath

    @property
    def status(self):
        return self._spec['status']

    @property
    def order_no(self):
        return self._spec['order_no']

    @inlineCallbacks
    def install(self):
        self.actual.resource_manager.insert(
            self.avatar_filename, url=self.avatar_url, rtype=ASSET)
        r = self.actual.resource_manager.get(self.avatar_filename)
        yield self.actual.resource_manager.prefetch(r)

    def uninstall(self):
        fname = os.path.basename(urlparse(self.avatar_url).path)
        self.actual.resource_manager.remove(fname)


class MultiWebApplicationsManager(object):
    def __init__(self, actual, *args, **kwargs):
        self._log = None
        self._actual = actual
        self._applications = []

    @property
    def actual(self):
        return self._actual

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="multiweb.manager", source=self)
        return self._log

    @inlineCallbacks
    def update(self, applications):
        self.log.info("Loading Applications Response with {n} Entries",
                      n=len(applications))
        self._applications = []
        for application in applications:
            app = MultiWebApplication(self, application)
            yield app.install()
            self._applications.append(app)
        self._applications.sort(key=lambda x: x.order_no)

    @property
    def applications(self):
        return [app for app in self._applications if app.status == 'ENABLE']
