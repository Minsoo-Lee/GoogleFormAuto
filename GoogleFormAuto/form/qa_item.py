from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web import webdriver

class QAItem:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QAItem, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if QAItem._initialized:
            return  # 이미 초기화된 경우, 바로 리턴
        # 전체 리스트 저장
        # 타입 / 질문 / 답변 / 기타 답변
        self.qa_items = []

        QAItem._initialized = True

    def save_qa(self, _type, _question, _answer, _etc=False):
        item = [_type, _question, _answer, _etc]
        self.qa_items.append(item)

    def get_qa_index(self, index):
        return self.qa_items[index]

    def get_qa(self):
        return self.qa_items

    def get_qa_length(self):
        return len(self.qa_items)

