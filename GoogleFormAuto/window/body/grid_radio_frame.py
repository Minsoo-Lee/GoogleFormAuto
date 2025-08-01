from utils.answer_type import AnswerType
from window.body.body_frame import BodyFrame
import wx

class GridRadioFrame(BodyFrame):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)

    def build_answer_section(self, answer=None):
        col_num = len(answer[0]) + 1
        row_num = len(answer[1]) + 1
        choice_list = [str(i) for i in range(1, col_num - 1)]

        # grid_box 제거 (테두리 하나만)
        grid_panel = wx.Panel(self.body_panel, wx.ID_ANY)
        grid_sizer = wx.FlexGridSizer(row_num, col_num, 10, 10)
        grid_sizer.AddGrowableCol(0, 1)
        # 모든 열 비율 0으로 (고정)
        # for i in range(col_num):
        #     print(i)
        #     grid_sizer.AddGrowableCol(i, 0)

        # 첫 행 (열 제목)
        empty_label = wx.StaticText(grid_panel, wx.ID_ANY, "", size=wx.Size(200, -1))
        grid_sizer.Add(empty_label, 0, wx.ALIGN_CENTER)
        for header in answer[0]:
            label = wx.StaticText(grid_panel, wx.ID_ANY, header, style=wx.ALIGN_CENTER)
            grid_sizer.Add(label, 0, wx.ALIGN_CENTER)

        # 나머지 행
        for choice in answer[1]:
            label = wx.StaticText(grid_panel, wx.ID_ANY, choice, size=wx.Size(200, -1))
            grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            tmp_list = []
            for i in range(col_num - 1):
                combo_box = wx.ComboBox(
                    grid_panel,
                    choices=choice_list,
                    style=wx.CB_READONLY,
                    size=wx.Size(40, -1)
                )
                if choice_list:  # 리스트가 비어있지 않다면
                    combo_box.SetSelection(0)  # 첫 번째 값 선택
                tmp_list.append(combo_box)
                grid_sizer.Add(combo_box, 0, wx.ALIGN_CENTER)  # EXPAND 제거, 가운데 정렬
            self.combo_list.append(tmp_list)

        grid_panel.SetSizer(grid_sizer)
        # 바로 answer_sizer에 추가
        self.answer_sizer.Add(grid_panel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.body_panel.Fit()

        return self.answer_sizer

    def save_prior_list(self):
        result = []
        result.append(AnswerType.GRID_RADIO)
        combo_values = []
        for combos in self.combo_list:
            tmp_list = []
            for combo in combos:
                tmp_list.append(int(combo.GetValue()))
            combo_values.append(tmp_list)
        result.append(combo_values)
        return result