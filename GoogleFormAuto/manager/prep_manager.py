import time
import traceback

from selenium.webdriver.common.by import By
from form.qa_item import QAItem
from utils.answer_type import  AnswerType
from utils.short_inivt_type import ShortInvitType
from web.webdriver import WebDriver

class PrepManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrepManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if PrepManager._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.webdriver = WebDriver()
        self.qa_item = QAItem()

        PrepManager._initialized = True

    def set_random_answers(self, question, title):
        ret = self.gridradio_options(question, title.text)
        if ret == -1:
            ret = self.gridcheckbox_options(question, title.text)
        if ret == -1:
            ret = self.radio_options(question, title.text)
        if ret == -1:
            ret = self.radio2_options(question, title.text)
        if ret == -1:
            ret = self.invitation_options(question, title.text)
        if ret == -1:
            ret = self.short_invitation_options(question, title.text)
        if ret == -1:
            ret = self.checkbox_options(question, title.text)
        if ret == -1:
            self.dropbox_options(question, title.text, WebDriver().get_driver())

    def gridradio_options(self, question, title):
        try:
            elements = question.find_element(By.CLASS_NAME, 'gTGYUd')
        except:
            return -1
        answers = []
        parent_element = elements.find_element(By.CSS_SELECTOR, '.ssX1Bd.KZt9Tc')
        child_elements = parent_element.find_elements(By.XPATH, "./*")

        column = []
        for child in child_elements:
            if child.text != '':
                column.append(child.text)
        #행
        row = []
        parent_elements = elements.find_elements(By.CSS_SELECTOR, '.lLfZXe.fnxRtf.EzyPc')
        if not parent_elements:
            return -1
        for parent in parent_elements:
            label = parent.get_attribute('aria-label')
            row.append(label)
            # print(label)
            parent.find_elements(By.CSS_SELECTOR, '.Od2TWd.hYsg7c')[0].click()

        answers.append(column)
        answers.append(row)

        self.qa_item.save_qa(AnswerType.GRID_RADIO, title, answers, None)
        return 1

    def gridcheckbox_options(self, question, title):
        try:
            elements = question.find_element(By.CLASS_NAME, 'gTGYUd')
        except:
            # print('gridrcheckbox x')
            return -1
        answers = []
        parent_element = elements.find_element(By.CSS_SELECTOR, '.ssX1Bd.KZt9Tc')
        child_elements = parent_element.find_elements(By.XPATH, "./*")  # Selects all child elements

        number_of_children = len(child_elements)
        # print(number_of_children)
        column = []
        for child in child_elements:
            if child.text != '':
                column.append(child.text)
            # print(child.text)
        #행
        row = []
        parent_elements = elements.find_elements(By.CSS_SELECTOR, '.V4d7Ke.wzWPxe.OIC90c')
        if not  parent_elements:
            # print('gridcheckbox x')
            return -1
        for parent in parent_elements:
            label = parent.text
            row.append(label)
            # print(label)

        elements = question.find_elements(By.CSS_SELECTOR, '.EzyPc.mxSrOe')
        for element in elements:
            click_elements = element.find_elements(By.CSS_SELECTOR, '.uVccjd.aiSeRd.wGQFbe.BJHAP')
            click_elements[0].click()

        answers.append(column)
        answers.append(row)

        self.qa_item.save_qa(AnswerType.GRID_CHECKBOX, title, answers, None)
        return 1

    def radio_options(self, question, title):
        answers = []
        child_elements = question.find_elements(By.CSS_SELECTOR, '.aDTYNe.snByac.OvPDhc.OIC90c')
        # 찾은 하위 요소들에 대해 원하는 작업을 수행합니다.
        if not child_elements:
            # print('radio x')
            return -1
        for child in child_elements:
            # 예를 들어, 각 하위 요소의 텍스트를 출력할 수 있습니다.
            # print(child.text)
            answers.append(child.text)
            # if (child.text == "예"):
            #     child.click()
        child_elements[0].click()

        self.qa_item.save_qa(AnswerType.RADIO, title, answers, None)
        return 1

    def radio2_options(self, question, title):
        try:
            question.find_element(By.CSS_SELECTOR, '.nWQGrd.zwllIb.zfdaxb')
        except Exception as e:
            return -1

        answers = []
        child_elements = question.find_elements(By.CSS_SELECTOR, '.aDTYNe.snByac.OvPDhc.OIC90c')
        # 찾은 하위 요소들에 대해 원하는 작업을 수행합니다.
        if not child_elements:
            return -1

        for child in child_elements:
            # 예를 들어, 각 하위 요소의 텍스트를 출력할 수 있습니다.
            # print(child.text)
            answers.append(child.text)
            # if (child.text == "예"):
            #     child.click()
        child_elements[0].click()

        self.qa_item.save_qa(AnswerType.RADIO2, title, answers, True)
        return 1

    def invitation_options(self, question, title):
        child_elements = question.find_elements(By.CSS_SELECTOR, '.KHxj8b.tL9Q4c')
        # 찾은 하위 요소들에 대해 원하는 작업을 수행합니다.
        if not child_elements:
            # print('invitation x')
            return -1
        # print('is invitation')
        time.sleep(1)
        child_elements[0].send_keys('1')

        self.qa_item.save_qa(AnswerType.INVIT, title, None, None)
        return 1

    def short_invitation_options(self, question, title):
        child_elements = question.find_elements(By.CSS_SELECTOR, '.whsOnd.zHQkBf')
        # 찾은 하위 요소들에 대해 원하는 작업을 수행합니다.
        if not child_elements:
            # print('short invitation x')
            return -1
        # print('is short invitation')

        child_elements[0].send_keys('1')

        if "키(cm)" in title or "몸무게(kg)" in title:
            self.qa_item.save_qa(AnswerType.SHORT_INVIT, title, ShortInvitType.MIN_MAX, None)
        else:
            self.qa_item.save_qa(AnswerType.SHORT_INVIT, title, ShortInvitType.PHONE, None)
        return 1

    def checkbox_options(self, question, title):
        answers = []
        child_elements = question.find_elements(By.CSS_SELECTOR, '.aDTYNe.snByac.n5vBHf.OIC90c')
        if not child_elements:
            # print('checkbox x')
            return -1
        i = 1
        for child in child_elements:
            # print(child.text)
            answers.append(child.text)
            i += 1

        child_elements[0].click()

        self.qa_item.save_qa(AnswerType.CHECKBOX, title, answers, None)
        return 1

    def dropbox_options(self, question, title, driver):
        answers = []
        elements = question.find_elements(By.CSS_SELECTOR, '.jgvuAb.ybOdnf.cGN2le.t9kgXb.llrsB')
        if not elements:
            return -1

        elements[0].click()
        time.sleep(1)
        listbox_elements = question.find_elements(By.CSS_SELECTOR, '.OA0qNb.ncFHed.QXL7Te')

        child_elements = listbox_elements[0].find_elements(By.CSS_SELECTOR, '.MocG8c.HZ3kWc.mhLiyf.OIC90c.LMgvRb')
        if not child_elements:
            return -1
        for child in child_elements:
            data_value = child.get_attribute('data-value')
            answers.append(data_value)

        self.webdriver.wait_until_clickable(10, child_elements[0])

        self.qa_item.save_qa(AnswerType.DROPBOX, title, answers, None)

        return 1