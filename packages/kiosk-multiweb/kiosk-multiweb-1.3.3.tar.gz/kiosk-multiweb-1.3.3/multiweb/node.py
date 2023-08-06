

import os
from kivy_garden.ebs.core.colors import GuiPalette
from starxmedia.node import StarXMediaNode

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.netconfig.mixin import NetconfigGuiMixin

from .api import MultiWebApiEngine
from .applications.mixins import MultiWebApplicationsMixin
from .applications.mixins import MultiWebApplicationsGuiMixin


class KioskMultiWebNode(NetconfigGuiMixin,
                        MultiWebApplicationsGuiMixin,
                        MultiWebApplicationsMixin,
                        StarXMediaNode):
    _palette = GuiPalette(
        background=(0xf7 / 255, 0xf7 / 255, 0xf7 / 255),
        foreground=(0xff / 255, 0xff / 255, 0xff / 255),
        color_1=(0x72 / 255., 0xc2 / 255., 0xf5 / 255., 1),
        color_2=(0x07 / 255., 0x3e / 255., 0xbc / 255., 1)
    )
    _gui_marquee_bgcolor = (0xff / 255., 0x00 / 255., 0x00 / 255., 0.6)
    _gui_supports_overlay_mode = True

    def install(self):
        super(KioskMultiWebNode, self).install()

        self.config.register_application_root(
            os.path.abspath(os.path.dirname(__file__))
        )

        _elements = {
            'multiweb_api_url': ElementSpec('multiweb', 'url', ItemSpec(str, fallback='https://apps.starxmedia.in/api/v1')),
        }

        for name, spec in _elements.items():
            self.config.register_element(name, spec)

        multiweb_api_engine = self.modapi_engine('multiweb')
        if not multiweb_api_engine:
            self.log.info("Installing Vanilla MultiWeb Api Engine")
            multiweb_api_engine = MultiWebApiEngine(self)
            self.modapi_install(multiweb_api_engine)

        multiweb_api_engine.install_task('api_applications_task', 1800)
