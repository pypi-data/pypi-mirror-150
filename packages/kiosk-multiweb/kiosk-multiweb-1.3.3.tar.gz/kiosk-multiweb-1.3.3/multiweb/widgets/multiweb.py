

from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from .panel import MultiWebApplicationsPanel
from .browser import ApplicationBrowser


class MultiWebPanel(object):
    def __init__(self, actual, **kwargs):
        self._panel_bgcolor = kwargs.pop("bgcolor", [1, 1, 1, 1])
        self._panel_button_bgcolor = kwargs.pop("button_color", 'auto')
        self._panel_minimum_apps = kwargs.pop("minimum_apps", 0)
        self._panel_cols = kwargs.pop("apps_per_row", 4)
        self._panel_pad_last_row = kwargs.pop("pad_last_row", False)
        self._panel_button_radius = kwargs.pop("button_radius", 0)
        self._block_heuristics = {
            'blank': kwargs.pop('block_heuristic_blank', False)
        }
        super(MultiWebPanel).__init__(**kwargs)
        self._actual = actual
        self._screen_manager = ScreenManager()

        self._application_screen = None
        self._application_spec = None
        self._application_browser = None

        self._applications_panel = None
        self._applications_panel_screen = None

        self._create_applications_panel()

    @property
    def actual(self):
        return self._actual

    @property
    def block_heuristics(self):
        return self._block_heuristics

    @property
    def panel_bgcolor(self):
        return self._panel_bgcolor

    @property
    def panel_button_bgcolor(self):
        return self._panel_button_bgcolor

    @property
    def applications_panel_screen(self):
        if not self._applications_panel_screen:
            self._applications_panel_screen = Screen(name="panel")
            self._applications_panel_screen.add_widget(self.applications_panel)
        return self._applications_panel_screen

    @property
    def applications_panel(self):
        if not self._applications_panel:
            self._applications_panel = MultiWebApplicationsPanel(
                self, bgcolor=self._panel_bgcolor,
                button_color=self._panel_button_bgcolor,
                button_radius=self._panel_button_radius,
                minimum_apps=self._panel_minimum_apps,
                cols=self._panel_cols or 'auto',
                pad_last_row=self._panel_pad_last_row,
            )
        return self._applications_panel

    def _create_applications_panel(self):
        self._screen_manager.add_widget(self.applications_panel_screen)

    def set_applications(self, applications):
        self.applications_panel.set_applications(applications)

    def launch_application(self, application):
        self._application_spec = application
        self.applications_panel.disable_panel()
        self._application_browser = ApplicationBrowser(self)
        self._application_browser.launch_application(application, self._on_load_complete)
        self.application_screen.add_widget(self._application_browser)
        self._application_browser.dialog_target = self.application_screen
        self._screen_manager.add_widget(self._application_screen)

    def _on_load_complete(self, *_):
        self._screen_manager.current = 'application'

    def close_application(self):
        self._screen_manager.current = 'panel'
        if self._screen_manager.has_screen('application'):
            self._screen_manager.remove_widget(self.application_screen)
        if self._application_screen:
            self._application_screen.clear_widgets()
            self._application_screen = None
        self.applications_panel.enable_panel()

    @property
    def application_screen(self):
        if not self._application_screen:
            self._application_screen = Screen(name='application')
        return self._application_screen

    @property
    def widget(self):
        return self._screen_manager
