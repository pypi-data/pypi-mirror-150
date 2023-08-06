

from kivy.uix.boxlayout import BoxLayout

from starxmedia.node import StarXMediaNode
from ebs.linuxnode.core.config import ElementSpec, ItemSpec

from .manager import MultiWebApplicationsManager
from ..widgets.multiweb import MultiWebPanel


class MultiWebApplicationsMixin(StarXMediaNode):
    def __init__(self, *args, **kwargs):
        super(MultiWebApplicationsMixin, self).__init__(*args, **kwargs)
        self._multiweb_applications = MultiWebApplicationsManager(self)

    def multiweb_applications_update(self, response):
        return self._multiweb_applications.update(response)


class MultiWebApplicationsGuiMixin(MultiWebApplicationsMixin, StarXMediaNode):
    def __init__(self, *args, **kwargs):
        super(MultiWebApplicationsGuiMixin, self).__init__(*args, **kwargs)
        self._gui_multiweb_root = None
        self._multiweb = None

    @property
    def gui_multiweb_root(self):
        if not self._gui_multiweb_root:
            self._gui_multiweb_root = BoxLayout(spacing=0, padding=[0])
            self.gui_content_root.add_widget(self._gui_multiweb_root)
        return self._gui_multiweb_root

    def install(self):
        super(MultiWebApplicationsGuiMixin, self).install()

        _elements = {
            'multiweb_panel_bgcolor': ElementSpec(
                'multiweb', 'panel_bgcolor', ItemSpec('kivy_color', fallback="1:1:1:1")),
            'multiweb_panel_button_bgcolor': ElementSpec(
                'multiweb', 'panel_button_bgcolor', ItemSpec('kivy_color', fallback="auto")),
            'multiweb_panel_button_radius': ElementSpec(
                'multiweb', 'panel_button_radius', ItemSpec(int, fallback=0)),
            'multiweb_minimum_apps': ElementSpec(
                'multiweb', 'minimum_apps', ItemSpec(int, fallback=0)),
            'multiweb_apps_per_row': ElementSpec(
                'multiweb', 'apps_per_row', ItemSpec(int, fallback=4)),
            'multiweb_pad_last_row': ElementSpec(
                'multiweb', 'pad_last_row', ItemSpec(bool, fallback=False)),
            'multiweb_block_heuristic_blank': ElementSpec(
                'multiweb', 'block_heuristic_blank', ItemSpec(bool, fallback=False)),
        }

        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    def gui_setup(self):
        # TODO Fix this
        self.gui_main_content.size_hint = (1, 0.4)
        # TODO Fix this
        self.gui_multiweb_root.size_hint = (1, 0.6)

        gui = super(MultiWebApplicationsGuiMixin, self).gui_setup()

        self._multiweb = MultiWebPanel(self, bgcolor=self.config.multiweb_panel_bgcolor,
                                       button_color=self.config.multiweb_panel_button_bgcolor,
                                       button_radius=self.config.multiweb_panel_button_radius,
                                       minimum_apps=self.config.multiweb_minimum_apps,
                                       apps_per_row=self.config.multiweb_apps_per_row,
                                       pad_last_row=self.config.multiweb_pad_last_row,
                                       block_heuristic_blank=self.config.multiweb_block_heuristic_blank)
        self.gui_multiweb_root.add_widget(self._multiweb.widget)
        return gui

    def multiweb_widget_update(self):
        self._multiweb.set_applications(self._multiweb_applications.applications)

    def multiweb_applications_update(self, response):
        d = self._multiweb_applications.update(response)
        d.addCallback(lambda x: self.multiweb_widget_update())
