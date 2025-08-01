from abc import ABC, abstractmethod
import wx

class BodyFrame(ABC):
    def __init__(self, parent_panel):
        self.parent_panel = parent_panel
        self.QUESTION_SIZE = wx.Size(280, 60)
        self.ANSWER_SIZE = wx.Size(280, 40)

        self.body_panel = wx.Panel(self.parent_panel, size=wx.Size(700, 500))

        # 질문 + 정답 섹션만 담는 sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.body_panel.SetSizerAndFit(self.main_sizer)

        self.answer_box = wx.StaticBox(self.body_panel)
        self.answer_sizer = wx.StaticBoxSizer(self.answer_box, wx.VERTICAL)

        # Combobox 리스트 => 우선순위 담는데 사용
        self.combo_list = []

    def build_question_section(self, question):
        question_box = wx.StaticBox(self.body_panel)
        question_sizer = wx.StaticBoxSizer(question_box, wx.VERTICAL)

        # 폭을 부모 패널에 맞게 변경
        # question_label = wx.StaticText(
        #     self.body_panel,
        #     label=question,
        #     style=wx.ALIGN_CENTER_HORIZONTAL,
        #     size=wx.Size(700, -1)  # 패널과 동일한 폭
        # )

        question_label = wx.TextCtrl(
            self.body_panel,
            value=question,
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE
        )

        # question_label.Wrap(680)

        question_sizer.Add(question_label, 0, wx.ALL | wx.EXPAND, 5)
        return question_sizer

    @abstractmethod
    def build_answer_section(self, answer):
        pass

    def assemble_body(self, question, answer, button_sizer, execute_button_sizer):
        self.main_sizer.Add(self.build_question_section(question), 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.build_answer_section(answer), 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(execute_button_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.body_panel.Layout()
        self.body_panel.Fit()

    def get_body_panel(self):
        return self.body_panel

    @abstractmethod
    def save_prior_list(self):
        pass