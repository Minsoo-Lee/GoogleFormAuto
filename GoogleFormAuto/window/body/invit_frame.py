from window.body.body_frame import BodyFrame
import wx

class InvitFrame(BodyFrame):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)

    def build_answer_section(self, answer=None):
        # StaticBox (답변 섹션 감싸기)
        answer_box = wx.StaticBox(self.body_panel)
        answer_sizer = wx.StaticBoxSizer(answer_box, wx.VERTICAL)

        # 멀티라인 텍스트 입력창
        text_ctrl = wx.TextCtrl(
            self.body_panel,
            style=wx.TE_MULTILINE | wx.TE_WORDWRAP  # 여러 줄 + 자동 줄바꿈
        )
        text_ctrl.SetMinSize(wx.Size(280, 100))  # 가로/세로 크기 (적당히 조정 가능)

        answer_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        return answer_sizer