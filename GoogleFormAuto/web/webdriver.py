import time

import wx
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriver, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if WebDriver._initialized:
            return

        self.driver = None

    def init_chrome(self):
        # if WebDriver._initialized:
        #     return
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 헤드리스 모드를 활성화합니다.
        chrome_options.add_argument("--disable-gpu")  # GPU 가속을 비활성화합니다. 일부 시스템에서 필요할 수 있습니다.
        chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화. 일부 시스템에서 필요할 수 있습니다.
        chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안함

        self.driver = webdriver.Chrome(options=chrome_options)
        WebDriver._initialized = True

    def click_element_by_xpath(self, xpath):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, xpath).click()
            print("button O")
        except:
            print("button X")
            return


    def get_elements_by_class_EC(self, timeout, path):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, path))
        )

    def get_elements_by_class(self, path):
        time.sleep(2)
        return self.driver.find_elements(By.CLASS_NAME, path)

    def get_element_by_css(self, element, path):
        if element:
            return element.find_element(By.CSS_SELECTOR, path)
        else:
            return self.driver.find_element(By.CSS_SELECTOR, path)

    def get_elements_by_css(self, element, path):
        if element:
            return element.find_elements(By.CSS_SELECTOR, path)
        else:
            return self.driver.find_elements(By.CSS_SELECTOR, path)

    def wait_until_clickable(self, timeout, element):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element)
        ).click()

    def get_driver(self):
        return self.driver

    def enter_url(self, url):
        self.driver.get(url)

    def quit_chrome(self):
        self.driver.quit()