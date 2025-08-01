import threading
import time
import traceback

import wx
from selenium.webdriver.remote.webelement import WebElement

from form.form_data import FormData
from form.prior_item import PriorItem
from form.qa_item import QAItem
from manager.prep_manager import PrepManager
from manager.task_manager import TaskManager
from utils.answer_type import AnswerType
from utils.short_inivt_type import ShortInvitType
from web import webdriver
from window.body.checkbox_frame import CheckboxFrame
from window.body.dropbox_frame import DropboxFrame
from window.body.grid_checkbox_frame import GridCheckboxFrame
from window.body.grid_radio_frame import GridRadioFrame
from window.body.invit_frame import InvitFrame
from window.body.radio_frame import RadioFrame, Radio2Frame
from window.body.short_invit_frame import ShortInvitFrame
from window.elements import Elements
from window.prepare_frame import PrepareFrame

BUTTON_SIZE = wx.Size(400, 30)
FORM_BUTTON_SIZE = wx.Size(800, 30)
WINDOW_SIZE = wx.Size(600, 1000)

class MainFrame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None, wx.ID_ANY, "Google Form", size=WINDOW_SIZE, style=style)
        self.SetMinSize(WINDOW_SIZE)
        self.SetMaxSize(WINDOW_SIZE)

        self.body_list = []

        self.body_panel_item = None

        # QAItems 인덱스
        self.index = 0

        # driver 호출 (종료 시 정상 종료를 위해)
        self.webdriver = webdriver.WebDriver()

        # elements 요소
        self.elements = Elements()

        # FormData
        self.form_data = FormData()

        # PrepManager
        self.prep_manager = PrepManager()

        # TaskManager
        self.task_manager = TaskManager()

        # QAItems
        self.qa_items = QAItem()

        # PriorItems
        self.prior_items = PriorItem()

        # Button
        self.execute_button = None
        self.next_button = None
        self.prev_button = None

        # 메인 panel & sizer
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)

        # Prepare 섹션 구성
        self.prepare_frame = PrepareFrame(self.panel)
        self.prepare_frame.build_prepare_section()
        self.prepare_panel = self.prepare_frame.get_prepare_panel()
        self.prepare_button = wx.Button(self.prepare_panel, label="구글 폼 정보 가져오기", size=FORM_BUTTON_SIZE)
        self.assemble_prepare_section()

        # # Body 섹션 구성
        # self.total_body_panel = wx.Panel(self.panel)
        # self.total_body_sizer = wx.BoxSizer(wx.VERTICAL)

        # 정답 타입을 구분하여 작업 수행
        self.answer_frame = [
            InvitFrame,
            ShortInvitFrame,
            RadioFrame,
            Radio2Frame,
            CheckboxFrame,
            DropboxFrame,
            GridRadioFrame,
            GridCheckboxFrame,
        ]

        # 레이아웃 조립
        self.assemble_sections()

        # 종료 이벤트 바인딩
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def assemble_prepare_section(self):
        self.prepare_button.Bind(wx.EVT_BUTTON, self.on_prepare_button_clicked)

        self.elements.set_prepare_button(self.prepare_button)

        prepare_sizer = self.prepare_frame.get_prepare_sizer()
        prepare_sizer.Add(self.prepare_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.prepare_panel.SetSizer(prepare_sizer)

    def assemble_sections(self):
        # Prepare panel 추가
        self.panel_sizer.Add(self.prepare_panel, 0, wx.EXPAND | wx.ALL, 5)

        # panel, frame 레이아웃 설정
        self.panel.SetSizer(self.panel_sizer)
        self.frame_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(self.frame_sizer)
        self.Layout()

        self.SetSize(WINDOW_SIZE)
        self.SetMinSize(WINDOW_SIZE)
        self.SetMaxSize(WINDOW_SIZE)

    # Binding 함수
    def on_prepare_button_clicked(self, event):
        if self.form_data.set_data(self.elements.get_url_text_value(), self.elements.get_count_text_value()) == -1:
            return
        print(f"url : {self.form_data.get_url()}")
        print(f"count : {self.form_data.get_count()}")
        self.prepare_button.Enable(False),
        def process_form():
            self.webdriver.init_chrome()
            form_url = self.form_data.get_url()
            try:
                self.webdriver.enter_url(form_url)
            except Exception as e:
                print(f"[오류 발생] {e}")
                print("존재하지 않는 링크입니다. 다시 확인해 주세요.")
            while True:
                try:
                    # all_questions: list[WebElement] = self.webdriver.get_elements_by_class_EC(10, "Qr7Oae")
                    all_questions: list[WebElement] = self.webdriver.get_elements_by_class("Qr7Oae")

                    for question in all_questions:
                        # 각 섹션 내의 질문 제목을 찾습니다.
                        question_title = self.webdriver.get_element_by_css(question, ".M7eMe")
                        # set_random_answers
                        self.prep_manager.set_random_answers(question, question_title)
                        time.sleep(1)
                    time.sleep(2)
                except Exception as e:
                    print(type(e).__name__)
                if not self.click_next_button_prepare():
                    break
            print("문제 및 정답을 모두 수집하였습니다.")
            wx.CallAfter(self.add_body)
            self.webdriver.driver.quit()

        threading.Thread(target=process_form, daemon=True).start()

    def add_body(self):
        if self.body_panel_item is not None:
            self.body_panel_item.Hide()
            self.panel_sizer.Detach(self.body_panel_item)
            # self.body_panel_item.Destroy()

        # QAItems에서 첫 아이템을 하나 꺼냄
        qa_item = self.qa_items.get_qa_index(self.index)
        # 문항의 타입 확인
        qa_type: AnswerType = qa_item[0]
        # 타입에 맞는 frame 객체 꺼냄
        body_frame = self.answer_frame[qa_type.value](self.panel)

        # body frame을 mainframe에 추가
        body_panel = body_frame.get_body_panel()

        # button_sizer 반환
        button_sizer = self.add_button(body_panel)
        execute_button_sizer = self.add_execute_button(body_panel)

        # 질문 + 정답 섹션 조립
        body_frame.assemble_body(qa_item[1], qa_item[2], button_sizer, execute_button_sizer)

        # body_panel 추가
        self.panel_sizer.Add(body_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.body_panel_item = body_panel

        self.body_list.append(body_frame)

        self.panel.SetSizer(self.panel_sizer)
        self.panel.Layout()
        self.Layout()

        if self.index == self.qa_items.get_qa_length() - 1:
            self.execute_button.Enable(True)
            self.next_button.Enable(False)

    def add_button(self, panel):
        # 세로 전체 배치
        button_sizer = wx.BoxSizer(wx.VERTICAL)

        # 균등 2열 GridSizer
        h_sizer = wx.GridSizer(rows=1, cols=2, hgap=10, vgap=0)

        # 이전 질문 버튼
        self.prev_button = wx.Button(panel, label="이전 질문")
        self.prev_button.SetMinSize(BUTTON_SIZE)
        self.prev_button.SetMaxSize(BUTTON_SIZE)
        self.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_body_button_clicked)
        if self.index == 0:
            self.prev_button.Enable(False)
        h_sizer.Add(self.prev_button, 0, wx.EXPAND | wx.ALL, 5)

        # 다음 질문 버튼
        self.next_button = wx.Button(panel, label="다음 질문")
        self.next_button.SetMinSize(BUTTON_SIZE)
        self.next_button.SetMaxSize(BUTTON_SIZE)
        self.next_button.Bind(wx.EVT_BUTTON, self.on_add_body_button_clicked)
        h_sizer.Add(self.next_button, 0, wx.EXPAND | wx.ALL, 5)

        # 가로 버튼 sizer를 세로 sizer에 추가
        button_sizer.Add(h_sizer, 0, wx.EXPAND | wx.ALL, 5)

        return button_sizer

    def add_execute_button(self, panel):
        # 세로 전체 배치
        button_sizer = wx.BoxSizer(wx.VERTICAL)

        # 가로로 버튼 배치
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 이전 질문 버튼
        self.execute_button = wx.Button(panel, label="설문지 응답 시작", size=FORM_BUTTON_SIZE)
        h_sizer.Add(self.execute_button, 0, wx.ALL, 5)
        self.execute_button.Bind(wx.EVT_BUTTON, self.on_execute_button_clicked)
        self.execute_button.Enable(False)

        # 가로 버튼 sizer를 세로 sizer에 추가
        button_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER)

        return button_sizer

    def on_execute_button_clicked(self, event):
        self.prior_items.get_prior_result()
        def process_form():
            for i in range(self.form_data.get_count()):
                self.webdriver.init_chrome()
                form_url = self.form_data.get_url()
                try:
                    self.webdriver.enter_url(form_url)
                except Exception as e:
                    print(f"[오류 발생] {e}")
                    print("존재하지 않는 링크입니다. 다시 확인해 주세요.")
                while True:
                    try:
                        # all_questions: list[WebElement] = self.webdriver.get_elements_by_class_EC(10, "Qr7Oae")
                        all_questions: list[WebElement] = self.webdriver.get_elements_by_class("Qr7Oae")

                        for question in all_questions:
                            # 각 섹션 내의 질문 제목을 찾습니다.
                            question_title = self.webdriver.get_element_by_css(question, ".M7eMe")
                            # set_random_answers
                            self.task_manager.set_prior_answers(question, question_title)
                            time.sleep(1)
                        time.sleep(5)
                    except Exception as e:
                        print("[예외 이름]", type(e).__name__)
                        print("[예외 메시지]", str(e))
                        print("[전체 스택트레이스]")
                        traceback.print_exc()
                    if not self.click_next_button_prepare():
                        break
                print("응답 작성을 완료하였습니다.")
                self.click_submit_button()
                time.sleep(1)
                self.webdriver.driver.quit()
                self.webdriver.driver.quit()
                self.prior_items.init_prior_items()
                self.task_manager.init_prior_index()

        threading.Thread(target=process_form, daemon=True).start()
        self.webdriver.driver.quit()

    def on_prev_body_button_clicked(self, event):
        self.index -= 1
        self.prior_items.del_prior_list(self.index)
        self.prior_items.print_prior_list()
        if self.index == 0:
            self.prev_button.Enable(False)
        self.add_prev_body()
        del self.body_list[self.index + 1]

    def add_prev_body(self):
        if self.body_panel_item is not None:
            self.body_panel_item.Hide()
            self.panel_sizer.Detach(self.body_panel_item)
            # self.body_panel_item.Destroy()

        self.body_panel_item = self.body_list[self.index].get_body_panel()
        self.body_panel_item.Show()

        self.panel_sizer.Add(self.body_list[self.index].get_body_panel(), 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.panel_sizer)
        self.panel.Layout()
        self.execute_button.Enable(False)
        self.next_button.Enable(True)

    def on_add_body_button_clicked(self, event):
        # for i in range(48):
        #     # time.sleep(1)
        #     if self.qa_items.get_qa_index(self.index)[0] == AnswerType.SHORT_INVIT\
        #             and self.body_list[self.index].get_type() == ShortInvitType.MIN_MAX:
        #         min_val = self.body_list[self.index].get_min_value()
        #         max_val = self.body_list[self.index].get_max_value()
        #
        #         # 1) 비어있는지 확인
        #         if not min_val or not max_val:
        #             wx.MessageBox("최소값과 최대값을 모두 입력해주세요.", "오류", wx.OK | wx.ICON_ERROR)
        #             return
        #
        #         # 2) 숫자인지 확인
        #         if not (min_val.isdigit() and max_val.isdigit()):
        #             wx.MessageBox("최소값과 최대값은 정수만 입력할 수 있습니다.", "오류", wx.OK | wx.ICON_ERROR)
        #             return
        #
        #         # 3) 정수 변환
        #         min_val = int(min_val)
        #         max_val = int(max_val)
        #
        #         # 4) 최소값 < 최대값 조건 확인
        #         if min_val >= max_val:
        #             wx.MessageBox("최소값은 최대값보다 작아야 합니다.", "오류", wx.OK | wx.ICON_ERROR)
        #             return
        #
        #     # prior_items에 현재 우선순위 저장
        #     self.prior_items.add_prior_list(self.body_list[self.index].save_prior_list())
        #     self.index += 1
        #
        #     if self.index >= self.qa_items.get_qa_length():
        #         wx.MessageBox("마지막 질문입니다.", "알림", wx.OK | wx.ICON_INFORMATION)
        #         return
        #
        #     # 다음 질문 인덱스
        #     self.add_body()  # 다시 호출


        #=========================================
        if self.qa_items.get_qa_index(self.index)[0] == AnswerType.SHORT_INVIT\
                and self.body_list[self.index].get_type() == ShortInvitType.MIN_MAX:
            min_val = self.body_list[self.index].get_min_value()
            max_val = self.body_list[self.index].get_max_value()

            # 1) 비어있는지 확인
            if not min_val or not max_val:
                wx.MessageBox("최소값과 최대값을 모두 입력해주세요.", "오류", wx.OK | wx.ICON_ERROR)
                return

            # 2) 숫자인지 확인
            if not (min_val.isdigit() and max_val.isdigit()):
                wx.MessageBox("최소값과 최대값은 정수만 입력할 수 있습니다.", "오류", wx.OK | wx.ICON_ERROR)
                return

            # 3) 정수 변환
            min_val = int(min_val)
            max_val = int(max_val)

            # 4) 최소값 < 최대값 조건 확인
            if min_val >= max_val:
                wx.MessageBox("최소값은 최대값보다 작아야 합니다.", "오류", wx.OK | wx.ICON_ERROR)
                return

        # prior_items에 현재 우선순위 저장
        self.prior_items.add_prior_list(self.body_list[self.index].save_prior_list())

        self.index += 1
        print(self.qa_items.get_qa_length())

        # 다음 질문 인덱스
        self.add_body()  # 다시 호출

    def click_submit_button(self):
        button_list = self.webdriver.get_elements_by_css(None, ".uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux")
        time.sleep(1)
        for button in button_list:
            spans = self.webdriver.get_elements_by_css(button, '.NPEfkd.RveJvd.snByac')
            for span in spans:
                if span.text.strip() == "제출":
                    button.click()

    def click_next_button_prepare(self):
        is_next_button = False
        button_list = self.webdriver.get_elements_by_css(None, ".uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux")
        for button in button_list:
            spans = self.webdriver.get_elements_by_css(button, '.NPEfkd.RveJvd.snByac')
            for span in spans:
                if span.text == "다음":
                    is_next_button = True
                    button.click()
        if not is_next_button:
            return False
        return True

    def on_close(self, event):
        # 리소스 정리 또는 확인 대화창 등을 여기에 넣을 수 있음
        self.Destroy()  # 프레임 제거
        self.webdriver.quit_chrome()
        wx.GetApp().ExitMainLoop()  # 메인 루프 종료 -> 프로세스 종료
