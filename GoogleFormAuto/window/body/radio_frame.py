from utils.answer_type import AnswerType
from window.body.body_frame import BodyFrame
import wx

class RadioFrame(BodyFrame):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)

    # def build_answer_section(self, answer):
    #     # answer_box = wx.StaticBox(self.body_panel)
    #     # answer_sizer = wx.StaticBoxSizer(answer_box, wx.VERTICAL)
    #     choice_list = [str(i) for i in range(1, len(answer) + 1)]
    #
    #     for a in answer:
    #         row_sizer = wx.BoxSizer(wx.HORIZONTAL)
    #         answer_label = wx.StaticText(self.body_panel, label=a, style=wx.ALIGN_CENTER_VERTICAL)
    #         answer_label.Wrap(self.ANSWER_SIZE.GetWidth())
    #         answer_label.SetSize(answer_label.GetBestSize())
    #         row_sizer.Add(answer_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
    #
    #         combo_box = wx.ComboBox(
    #             self.body_panel,
    #             choices=choice_list,
    #             style=wx.CB_READONLY,
    #             size=wx.Size(40, -1)
    #         )
    #         self.combo_list.append(combo_box)
    #         row_sizer.Add(combo_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
    #         self.answer_sizer.Add(row_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
    #
    #     # 여기서도 SetSizer 안 함 → 반환만
    #     return self.answer_sizer

    def build_answer_section(self, answer):
        choice_list = [str(i) for i in range(0, len(answer) + 1)]
        row_num = len(answer)
        # grid_box 제거 (테두리 하나만)
        grid_panel = wx.Panel(self.body_panel, wx.ID_ANY)
        grid_sizer = wx.FlexGridSizer(row_num, 2, 10, 10)
        grid_sizer.AddGrowableCol(0, 1)

        for choice in answer:
            label = wx.StaticText(grid_panel, wx.ID_ANY, choice, size=wx.Size(400, -1))
            grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            combo_box = wx.ComboBox(
                grid_panel,
                choices=choice_list,
                style=wx.CB_READONLY,
                size=wx.Size(40, -1)
            )
            combo_box.SetSelection(1)
            grid_sizer.Add(combo_box, 0, wx.ALIGN_CENTER)  # EXPAND 제거, 가운데 정렬
            self.combo_list.append(combo_box)

        grid_panel.SetSizer(grid_sizer)
        # 바로 answer_sizer에 추가
        self.answer_sizer.Add(grid_panel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.body_panel.Fit()

        return self.answer_sizer

    def save_prior_list(self):
        result = []
        result.append(AnswerType.RADIO)
        combo_values = []
        for combo in self.combo_list:
            combo_values.append(int(combo.GetValue()))
        result.append(combo_values)
        return result

class Radio2Frame(BodyFrame):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)
        self.text_input = None

    def build_answer_section(self, answer):
        choice_list = [str(i) for i in range(1, len(answer) + 1)]

        for a in answer:
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            etc_label = wx.StaticText(self.body_panel, label=a, style=wx.ALIGN_CENTER_VERTICAL)
            etc_label.Wrap(self.ANSWER_SIZE.GetWidth())
            etc_label.SetSize(etc_label.GetBestSize())
            row_sizer.Add(etc_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

            row_sizer.AddStretchSpacer()

            combo_box = wx.ComboBox(
                self.body_panel,
                choices=choice_list,
                style=wx.CB_READONLY,
                size=wx.Size(40, -1)
            )
            self.combo_list.append(combo_box)
            row_sizer.Add(combo_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.answer_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        etc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        etc_label = wx.StaticText(self.body_panel, label="기타: ", style=wx.ALIGN_CENTER_VERTICAL)
        etc_label.Wrap(self.ANSWER_SIZE.GetWidth())
        etc_label.SetSize(etc_label.GetBestSize())
        etc_sizer.Add(etc_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        etc_sizer.AddStretchSpacer()

        # **텍스트 입력창 추가**
        etc_text = wx.TextCtrl(
            self.body_panel,
            value="",  # 초기값
            size=wx.Size(200, -1)  # 적당한 너비
        )
        etc_sizer.Add(etc_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.text_input = etc_text

        etc_sizer.AddStretchSpacer()

        combo_box = wx.ComboBox(
            self.body_panel,
            choices=choice_list,
            style=wx.CB_READONLY,
            size=wx.Size(40, -1)
        )
        etc_sizer.Add(combo_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.combo_list.append(combo_box)

        self.answer_sizer.Add(etc_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 여기서도 SetSizer 안 함 → 반환만
        return self.answer_sizer

    def save_prior_list(self):
        result = []
        result.append(AnswerType.RADIO2)
        combo_values = []
        for combo in self.combo_list:
            combo_values.append(combo.GetValue())
        result.append(combo_values)
        result.append(self.text_input.GetValue())
        return result
