import wx
from utils.binding import Binding
from window.elements import (Elements)

LABEL_SIZE = wx.Size(70, 20)
INPUT_SIZE = wx.Size(200, 20)

class PrepareFrame:
    def __init__(self, parent_panel):
        self.parent_panel = parent_panel

        self.prepare_panel = wx.Panel(self.parent_panel)
        self.prepare_sizer = wx.BoxSizer(wx.VERTICAL)

        self.url_panel = wx.Panel(self.prepare_panel)
        self.count_panel = wx.Panel(self.prepare_panel)

        # Binding 함수
        self.binding = Binding()

        # elements 요소
        self.elements = Elements()

    def build_prepare_section(self):
        # Count 영역
        count_box = wx.BoxSizer(wx.HORIZONTAL)
        count_label = wx.StaticText(self.prepare_panel, label="반복 횟수", size=LABEL_SIZE,
                               style=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        count_input = wx.TextCtrl(self.prepare_panel, size=INPUT_SIZE)
        count_box.Add(count_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        count_box.Add(count_input, 1, wx.ALL | wx.EXPAND, 5)

        self.elements.set_count_text(count_input)

        # Url 영역
        url_box = wx.BoxSizer(wx.HORIZONTAL)
        url_label = wx.StaticText(self.prepare_panel, label="URL", size=LABEL_SIZE,
                               style=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        url_input = wx.TextCtrl(self.prepare_panel, size=INPUT_SIZE)
        url_box.Add(url_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        url_box.Add(url_input, 1, wx.ALL | wx.EXPAND, 5)

        self.elements.set_url_text(url_input)

        # # --- 버튼 행 ---
        # prepare_button = wx.Button(self.prepare_panel, label="구글 폼 정보 가져오기", size=BUTTON_SIZE)
        # prepare_button.Bind(wx.EVT_BUTTON, self.binding.on_prepare_button_clicked)
        #
        # self.elements.set_prepare_button(prepare_button)

        # --- 메인에 추가 ---
        self.prepare_sizer.Add(count_box, 0, wx.EXPAND)
        self.prepare_sizer.Add(url_box, 0, wx.EXPAND)
        # self.prepare_sizer.Add(prepare_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.prepare_panel.SetSizer(self.prepare_sizer)

        # 테스트
        url_input.SetValue("https://docs.google.com/forms/d/e/1FAIpQLSd5W8UY-eYFnU44b6SIvF8GrbLYple_1V9iinmH5-v-VUWUBg/viewform")

    def get_prepare_panel(self):
        return self.prepare_panel

    def get_prepare_sizer(self):
        return self.prepare_sizer





