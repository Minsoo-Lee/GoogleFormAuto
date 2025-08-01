import time
from selenium.webdriver.remote.webelement import WebElement
from window import elements
from web import webdriver
from manager.prep_manager import PrepManager
from form.qa_item import QAItem

class Binding:
    def __init__(self):
        # Elements 속성
        self.elements = elements.Elements()

        # WebDriver
        self.webdriver = webdriver.WebDriver()

        # PrepManager
        self.prep_manager = PrepManager()

        # QAItems
        self.qa_items = QAItem()

    def on_prepare_button_clicked(self, event):
        self.webdriver.init_chrome()
        form_url = self.elements.get_url_text_value()
        try:
            self.webdriver.enter_url(form_url)
        except Exception as e:
            print(f"[오류 발생] {e}")
            print("존재하지 않는 링크입니다. 다시 확인해 주세요.")
        while True:
            try:
                all_questions: list[WebElement] = self.webdriver.get_elements_by_class_EC(10, "Qr7Oae")
                for question in all_questions:
                    # 각 섹션 내의 질문 제목을 찾습니다.
                    question_title = self.webdriver.get_element_by_css(question, ".M7eMe")
                    # set_random_answers
                    self.prep_manager.set_random_answers(question, question_title)
                time.sleep(10)
            except Exception as e:
                pass
            if not self.click_next_button_prepare():
                break
        print(self.qa_items.get_qa())

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


