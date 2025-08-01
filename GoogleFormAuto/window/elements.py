import wx

class Elements:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Elements, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if Elements._initialized:
            return

        # Prepare 섹션
        self.count_text: wx.TextCtrl = None
        self.url_text: wx.TextCtrl = None
        self.prepare_button: wx.Button = None

        # Body 섹션
        Elements._initialized = True

    # Setter
    def set_count_text(self, count_text: wx.TextCtrl):
        self.count_text = count_text

    def set_url_text(self, url_text: wx.TextCtrl):
        self.url_text = url_text

    def set_prepare_button(self, prepare_button: wx.Button):
        self.prepare_button = prepare_button

    # Value getter
    def get_count_text_value(self):
        return self.count_text.GetValue()

    def get_url_text_value(self):
        return self.url_text.GetValue()
