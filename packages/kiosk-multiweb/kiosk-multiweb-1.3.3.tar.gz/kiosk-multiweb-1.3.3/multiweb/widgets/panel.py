

import math
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy_garden.ebs.progressspinner import TextureProgressSpinner
from kivy_garden.ebs.core.colors import BackgroundColorMixin
from kivy_garden.ebs.core.colors import RoundedColorBoxLayout
from kivy_garden.ebs.core.buttons import RoundedBleedImageButton


class MultiWebApplicationsPanel(BackgroundColorMixin, GridLayout):
    _disabled_opacity = 0.5
    _normal_opacity = 1

    def __init__(self, manager, **kwargs):
        self._manager = manager
        kwargs.setdefault('cols', 4)
        if kwargs['cols'] == 'auto':
            kwargs['cols'] = 4
            self._adaptive_layout = True
        else:
            self._adaptive_layout = False
        kwargs.setdefault('padding', [30])
        kwargs.setdefault('spacing', [15])
        bg_color = kwargs.pop('bgcolor', [1, 1, 1, 1])
        r = kwargs.pop('button_radius', 0)
        self._button_radius = [(r, r), (r, r), (r, r), (r,r)]
        self._button_color = kwargs.pop('button_color', 'auto')
        self._minimum_apps = kwargs.pop('minimum_apps', 0)
        self._pad_last_row = kwargs.pop('pad_last_row', False)
        GridLayout.__init__(self, **kwargs)
        BackgroundColorMixin.__init__(self, bgcolor=bg_color)
        self._applications = []
        self._buttons = []
        self._extra_blocks = []
        self._busy_spinner = None

    @property
    def busy_spinner(self):
        if not self._busy_spinner:
            self._busy_spinner = TextureProgressSpinner(
                size_hint=(0.4, 0.4), color=[0.4, 0.4, 0.4],
                pos_hint= {'center_x': 0.5, 'center_y': 0.5}
            )
        return self._busy_spinner

    @property
    def _base_opacity(self):
        if self._button_color == 'auto':
            return 0.3
        else:
            return 1

    @property
    def _highlight_opacity(self):
        if self._button_color == 'auto':
            return 0.8
        else:
            return 0.7

    def disable_panel(self):
        for button in self._buttons:
            button.disabled = True
            button.opacity = self._disabled_opacity
        for block in self._extra_blocks:
            block.opacity = self._disabled_opacity
        self.parent.add_widget(self.busy_spinner)

    def enable_panel(self):
        for button in self._buttons:
            button.disabled = False
            button.opacity = self._normal_opacity
        for block in self._extra_blocks:
            block.opacity = self._normal_opacity
        self.parent.remove_widget(self.busy_spinner)
        self._busy_spinner = None

    def _button_state_handler(self, button, state):
        if state == "normal":
            button.set_bgopacity(self._base_opacity)
        elif state == "down":
            button.set_bgopacity(self._highlight_opacity)

    def _button_press_handler(self, application):
        pass

    def _button_release_handler(self, application):
        self._manager.launch_application(application)

    def _optimize_layout(self, napps):
        return math.ceil(math.sqrt(napps))

    def set_applications(self, applications):
        self._applications = []
        self._extra_blocks = []
        self._buttons = []
        self.clear_widgets()

        if self._adaptive_layout:
            napps = max(len(applications), self._minimum_apps)
            self.cols = self._optimize_layout(napps)

        for app in applications:
            print("Creating application", app)
            self._applications.append(app)
            app_button = RoundedBleedImageButton(source=app.avatar, bgcolor=self._button_color,
                                                 radius=self._button_radius)
            app_button.set_bgopacity(self._base_opacity)
            app_button.on_press = partial(self._button_press_handler, app)
            app_button.on_release = partial(self._button_release_handler, app)
            app_button.bind(state=self._button_state_handler)
            self._buttons.append(app_button)
            self.add_widget(app_button)

        bgcolor = self._button_color
        if bgcolor == 'auto':
            bgcolor = (1, 1, 1, 1)

        if len(self._applications) < self._minimum_apps:
            for i in range(self._minimum_apps - len(self._applications)):
                eblock = RoundedColorBoxLayout(bgcolor=bgcolor, radius=self._button_radius)
                self.add_widget(eblock)
                self._extra_blocks.append(eblock)
            n_places = self._minimum_apps
        else:
            n_places = len(self._applications)

        if self._pad_last_row:
            extra_blocks = round((math.ceil(n_places / self.cols) - (n_places / self.cols)) * self.cols)
            for i in range(extra_blocks):
                eblock = RoundedColorBoxLayout(bgcolor=bgcolor, radius=self._button_radius)
                self.add_widget(eblock)
                self._extra_blocks.append(eblock)
