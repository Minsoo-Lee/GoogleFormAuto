import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="폼 예제", size=(300, 200))

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)  # 전체 세로 배치

        # --- 첫 번째 행 ---
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, label="이름:")
        input1 = wx.TextCtrl(panel)
        row1.Add(label1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        row1.Add(input1, 1, wx.ALL | wx.EXPAND, 5)

        # --- 두 번째 행 ---
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label="이메일:")
        input2 = wx.TextCtrl(panel)
        row2.Add(label2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        row2.Add(input2, 1, wx.ALL | wx.EXPAND, 5)

        # --- 버튼 행 ---
        button = wx.Button(panel, label="확인")

        # --- 메인에 추가 ---
        main_sizer.Add(row1, 0, wx.EXPAND)
        main_sizer.Add(row2, 0, wx.EXPAND)
        main_sizer.Add(button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(main_sizer)
        self.Centre()

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()