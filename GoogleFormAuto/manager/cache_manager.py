import time
import traceback

from selenium.webdriver.common.by import By
from form.qa_item import QAItem
from utils.answer_type import  AnswerType
from utils.short_inivt_type import ShortInvitType
from web.webdriver import WebDriver

class CacheManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if CacheManager._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.cache_data = []

        CacheManager._initialized = True

    def save_data_internal(self, index, data):
        pass

    def download_data_to_external(self):
        pass

