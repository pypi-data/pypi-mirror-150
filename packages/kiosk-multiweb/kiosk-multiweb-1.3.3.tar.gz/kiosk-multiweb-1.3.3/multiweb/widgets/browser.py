

import os
from kivy_garden.ebs.cefkivy.browser import CefBrowser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy_garden.ebs.progressspinner import TextureProgressSpinner

from kivy_garden.ebs.core.colors import ColorBoxLayout
from kivy_garden.ebs.core.buttons import BleedImageButton

from kivy_garden.ebs.cefkivy.handlers.display import DisplayHandler
from kivy_garden.ebs.cefkivy.handlers.download import DownloadHandler
from kivy_garden.ebs.cefkivy.handlers.jsdialog import JavascriptDialogHandler
from kivy_garden.ebs.cefkivy.handlers.keyboard import KeyboardHandler
from kivy_garden.ebs.cefkivy.handlers.lifespan import LifespanHandler
from kivy_garden.ebs.cefkivy.handlers.load import LoadHandler
from kivy_garden.ebs.cefkivy.handlers.render import RenderHandler
from kivy_garden.ebs.cefkivy.handlers.request import RequestHandler

from .blockdialog import FilterBlockDialog
from .blockdialog import SimplePopupBlockDialog


class FilteringRequestHandler(RequestHandler):

    def _check_url_blacklist(self, url):
        if self._widget.blacklist_urls:
            for blacklisted in self._widget.blacklist_urls:
                if url.startswith(blacklisted):
                    self.log.info("Blacklisting due to : {blacklist_entry}",
                                  blacklist_entry=blacklisted)
                    return True
        return False

    def _check_url_whitelist(self, url):
        if self._widget.whitelist_urls:
            for whitelisted in self._widget.whitelist_urls:
                if url.startswith(whitelisted):
                    self.log.info("Whitelisting due to : {whitelist_entry}",
                                  whitelist_entry=whitelisted)
                    return False
        self.log.debug("Not on whitelist : {whitelist}", whitelist=self._widget.whitelist_urls)
        return True

    def _check_url(self, url):
        blacklisted = self._check_url_blacklist(url)
        if blacklisted:
            return True
        blocked = self._check_url_whitelist(url)
        if blocked:
            return True
        return False

    def _block(self, url):
        block_dialog = FilterBlockDialog(browser=self._widget.browser, callback=None,
                                         message_text=url)
        self._widget.dialog_show(block_dialog)
        return True

    def _allow(self, url):
        return False

    @property
    def _blank_heuristic_enabled(self):
        if 'blank' in self._widget.block_heuristics and self._widget.block_heuristics['blank']:
            return True
        if '*' in self._widget.whitelist_urls:
            return True
        return False

    def OnBeforeBrowse(self, browser, frame, request, user_gesture, is_redirect):
        super(FilteringRequestHandler, self).OnBeforeBrowse(browser, frame, request, user_gesture, is_redirect)

        blacklisted = self._check_url_blacklist(request.GetUrl())
        if blacklisted:
            return self._block(request.GetUrl())

        if not user_gesture:
            self.log.debug("Automatic Browse to : {url}", url=request.GetUrl())
            return self._allow(request.GetUrl())

        self.log.debug("User Browsing To : {url}", url=request.GetUrl())

        if self._blank_heuristic_enabled:
            self.log.info("noblank Allowed Browse to : {url}", url=request.GetUrl())
            # Only block anything that is effectively a target:blank. i.e., only block popups.
            return self._allow(request.GetUrl())

        blocked = self._check_url_whitelist(request.GetUrl())
        if blocked:
            return self._block(request.GetUrl())
        return self._allow(request.GetUrl())

    def OnBeforeResourceLoad(self, browser, frame, request):
        super(FilteringRequestHandler, self).OnBeforeResourceLoad(browser, frame, request)
        self.log.debug("Getting Resource : {url}", url=request.GetUrl())
        # return self._check_url(request.GetUrl())
        return False


class FilteringBrowser(CefBrowser):

    _popup_block_dialog_class = SimplePopupBlockDialog

    _handlers = [
        DisplayHandler,
        DownloadHandler,
        JavascriptDialogHandler,
        KeyboardHandler,
        LifespanHandler,
        LoadHandler,
        RenderHandler,
        FilteringRequestHandler,
    ]

    def __init__(self, **kwargs):
        self._whitelist_urls = kwargs.pop('whitelist_urls', [])
        self._blacklist_urls = kwargs.pop('blacklist_urls', [])
        self._block_heuristics = kwargs.pop('block_heuristics', {})
        super(FilteringBrowser, self).__init__(**kwargs)

    @property
    def block_heuristics(self):
        return self._block_heuristics

    @property
    def whitelist_urls(self):
        return self._whitelist_urls

    @property
    def blacklist_urls(self):
        return self._blacklist_urls


class LoadMonitoredFilteringBrowser(FilteringBrowser):
    def __init__(self, **kwargs):
        super(LoadMonitoredFilteringBrowser, self).__init__(**kwargs)
        self._on_ready_singleshot = None
        self._on_state_callback = None

    def on_ready_singleshot(self, callback):
        self._on_ready_singleshot = callback

    def on_state_update(self, callback):
        self._on_state_callback = callback

    def on_loading_state_change(self, isLoading, canGoBack, canGoForward):
        super(LoadMonitoredFilteringBrowser, self).on_loading_state_change(isLoading, canGoBack, canGoForward)
        if self._on_ready_singleshot and not isLoading:
            self._on_ready_singleshot()
            self._on_ready_singleshot = None
        if self._on_state_callback:
            self._on_state_callback(isLoading, canGoBack, canGoForward)


class ApplicationBrowser(ColorBoxLayout):
    _nav_disabled_opacity = 0.1
    _nav_enabled_opacity = 1

    def __init__(self, manager, **kwargs):
        kwargs.setdefault('bgcolor', (1, 1, 1, 1))
        # TODO Fix this
        kwargs.setdefault('orientation', 'vertical')
        super(ApplicationBrowser, self).__init__(**kwargs)
        self._dialog_target = None
        self._manager = manager
        self._browser = None
        self._nav_bar = None
        self._nav_container = None
        self._nav_layout = None
        self._home_button = None
        self._back_button = None
        self._forward_button = None
        self._busy_spinner = None
        self._busy_shown = False
        self._create_nav_bar()

    def go_back(self):
        if self._browser:
            self._browser.browser.GoBack()

    def go_forward(self):
        if self._browser:
            self._browser.browser.GoForward()

    def _create_nav_bar(self):
        self._nav_bar = ColorBoxLayout(orientation='horizontal', size_hint=(1, 0.07),
                                       bgcolor=(0x72 / 255., 0xc2 / 255., 0xf5 / 255., 1))

        self._nav_layout = RelativeLayout(size_hint=(1, 1))

        _spacing = 10

        self._nav_container = BoxLayout(
            orientation="horizontal", pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=[10], spacing=_spacing, size_hint=(None, 1),
        )
        self._nav_container.add_widget(self.back_button)
        self._nav_container.add_widget(self.home_button)
        self._nav_container.add_widget(self.forward_button)

        def _rescale(*_):
            self._nav_container.width = self.back_button.width + self.home_button.width + \
                                        self.forward_button.width + _spacing * 2
        _rescale()
        self._nav_container.bind(on_size=_rescale)

        self._nav_layout.add_widget(self._nav_container)

        self._nav_bar.add_widget(self._nav_layout)
        self.add_widget(self._nav_bar)

    @property
    def busy_spinner(self):
        if not self._busy_spinner:
            self._busy_spinner = TextureProgressSpinner(
                size_hint=(1, 0.8), color=[0.4, 0.4, 0.4],
                pos_hint={'center_x': 0.9, 'center_y': 0.5}
            )
        return self._busy_spinner

    @property
    def home_button(self):
        if not self._home_button:
            home_button = self._manager.actual.config.get_path(os.path.join('resources', 'home.png'))
            self._home_button = BleedImageButton(source=home_button, bgcolor=(1, 1, 1, 0.1),
                                                 size_hint=(None, 1), keep_ratio=True)
            self._home_button.on_press = self._manager.close_application
        return self._home_button

    @property
    def back_button(self):
        if not self._back_button:
            back_button = self._manager.actual.config.get_path(os.path.join('resources', 'back.png'))
            self._back_button = BleedImageButton(source=back_button, bgcolor=(1, 1, 1, 0.1),
                                                 size_hint=(None, 1), keep_ratio=True)
            self._back_button.on_press = self.go_back
        return self._back_button

    @property
    def forward_button(self):
        if not self._forward_button:
            forward_button = self._manager.actual.config.get_path(os.path.join('resources', 'forward.png'))
            self._forward_button = BleedImageButton(source=forward_button, bgcolor=(1, 1, 1, 0.1),
                                                    size_hint=(None, 1), keep_ratio=True)
            self._forward_button.on_press = self.go_forward
        return self._forward_button

    def _update_nav_bar(self, is_loading, can_go_back, can_go_forward):
        if is_loading:
            self._nav_layout.add_widget(self.busy_spinner)
            self._busy_shown = True
        elif self._busy_shown:
            self._nav_layout.remove_widget(self.busy_spinner)
            self._busy_shown = False

        if can_go_back:
            self.enable_back_button()
        else:
            self.disable_back_button()

        if can_go_forward:
            self.enable_forward_button()
        else:
            self.disable_forward_button()

    def disable_back_button(self):
        self.back_button.disabled = True
        self.back_button.opacity = self._nav_disabled_opacity

    def enable_back_button(self):
        self.back_button.disabled = False
        self.back_button.opacity = self._nav_enabled_opacity

    def disable_forward_button(self):
        self.forward_button.disabled = True
        self.forward_button.opacity = self._nav_disabled_opacity

    def enable_forward_button(self):
        self.forward_button.disabled = False
        self.forward_button.opacity = self._nav_enabled_opacity

    @property
    def dialog_target(self):
        return self._dialog_target

    @dialog_target.setter
    def dialog_target(self, value):
        self._dialog_target = value
        self._browser.dialog_target = value

    def launch_application(self, application, callback):
        self._browser = LoadMonitoredFilteringBrowser(
            start_url=application.url,
            whitelist_urls=application.whitelist_urls,
            blacklist_urls=application.blacklist_urls,
            dialog_target=self.dialog_target,
            block_heuristics=self._manager.block_heuristics
        )
        self._browser.on_ready_singleshot(callback)
        self._browser.on_state_update(self._update_nav_bar)
        self.add_widget(self._browser, index=1)
