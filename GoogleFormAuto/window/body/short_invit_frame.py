import random

from utils.answer_type import AnswerType
from utils.short_inivt_type import ShortInvitType
from window.body.body_frame import BodyFrame
import wx

class ShortInvitFrame(BodyFrame):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)
        self.min_input = None
        self.max_input = None

        self.type = None

    def build_answer_section(self, answer=None):
        if answer == ShortInvitType.MIN_MAX:
            self.type = ShortInvitType.MIN_MAX
            self.build_answer_section_minmax()
        if answer == ShortInvitType.PHONE:
            self.type = ShortInvitType.PHONE
            self.build_answer_section_phone()

        # 여기서도 SetSizer 안 함 → 반환만
        return self.answer_sizer

    def build_answer_section_minmax(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 최소값
        min_label = wx.StaticText(self.body_panel, label="최소값")
        min_input = wx.TextCtrl(self.body_panel, size=wx.Size(80, -1))
        min_input.SetValue("150")

        # 최대값
        max_label = wx.StaticText(self.body_panel, label="최대값")
        max_input = wx.TextCtrl(self.body_panel, size=wx.Size(80, -1))
        max_input.SetValue("180")


        # 추가 (간격 조정: min_input과 max_label 사이에만 큰 간격)
        hbox.Add(min_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        hbox.Add(min_input, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 40)  # <-- 여기만 크게 띄움
        hbox.Add(max_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        hbox.Add(max_input, 0, wx.ALIGN_CENTER_VERTICAL)

        self.min_input = min_input
        self.max_input = max_input

        # 원래 answer_sizer에 추가
        self.answer_sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

    def build_answer_section_phone(self):
        # # 텍스트 달랑
        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        #
        # only_label = wx.StaticText(self.body_panel, label="최소값")  # 라벨 하나만
        # hbox.Add(only_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        #
        # self.answer_sizer.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)

        # 하나만 크게
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        only_label = wx.StaticText(self.body_panel, label="핸드폰 번호는 무작위로 생성합니다.")
        hbox.AddStretchSpacer(1)  # 좌측 여백
        hbox.Add(only_label, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.AddStretchSpacer(1)  # 우측 여백

        self.answer_sizer.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)

    def save_prior_list(self):
        result = []
        result.append(AnswerType.SHORT_INVIT)
        if self.type == ShortInvitType.MIN_MAX:
            result.append(ShortInvitType.MIN_MAX)
            value = [int(self.min_input.GetValue()), int(self.max_input.GetValue())]
            result.append(value)
        # 핸드폰 번호 무작위로 생성하여 삽
        else:
            def generate_phone():
                mid = str(random.randint(0, 9999)).zfill(4)  # 중간번호 4자리
                last = str(random.randint(0, 9999)).zfill(4)  # 끝번호 4자리
                return f"010-{mid}-{last}"
            result.append(ShortInvitType.PHONE)
            phone_num = generate_phone()
            result.append(phone_num)
        return result

    def get_min_value(self):
        return self.min_input.GetValue()

    def get_max_value(self):
        return self.max_input.GetValue()

    def get_type(self):
        return self.type

