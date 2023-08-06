

from kivy_garden.ebs.cefkivy.components.blockdialog import BlockDialog


class FilterBlockDialog(BlockDialog):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', "Access Denied")
        kwargs['message_text'] = "A link you clicked on attempted to redirect to another website.\n " \
                                 "Access to this link is not allowed on this browser.  " \
                                 "".format(kwargs['message_text'])
        super(FilterBlockDialog, self).__init__(**kwargs)


class SimplePopupBlockDialog(BlockDialog):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', "Popup Blocked")
        kwargs['message_text'] = "The website attempted to open a popup which was blocked." \
                                 "".format(kwargs['message_text'])
        super(SimplePopupBlockDialog, self).__init__(**kwargs)
