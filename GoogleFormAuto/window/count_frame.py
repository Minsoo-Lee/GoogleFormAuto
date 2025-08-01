import wx

class CountFrame:
    def __init__(self, parent_panel):
        self.parent_panel = parent_panel

        self.count_panel = wx.Panel(self.parent_panel)
        self.count_sizer = wx.BoxSizer(wx.VERTICAL)

    def build_count_section(self):
        box = wx.StaticBox(self.count_panel)
        self.count_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        count_input_label = wx.StaticText(self.count_panel, wx.ID_ANY, "작업 횟수 :", size=wx.Size(50, 20))
        url_input = wx.TextCtrl(self.count_panel)

        url_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        url_input_sizer.Add(count_input_label, 0, wx.ALIGN_CENTER_VERTICAL)  # 오른쪽만 간격 5
        url_input_sizer.Add(url_input, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # proportion=0으로 고정폭
        url_input.SetMinSize(wx.Size(300, -1))  # 입력창 고정 폭 (예: 300px)

        self.count_sizer.Add(url_input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.count_panel.SetSizer(self.count_sizer)

    def get_count_panel(self):
        return self.count_panel






