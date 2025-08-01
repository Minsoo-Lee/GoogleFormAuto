import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from web.webdriver import WebDriver

webdriver = WebDriver()
webdriver.init_chrome()
webdriver.enter_url("https://docs.google.com/forms/d/e/1FAIpQLSd5W8UY-eYFnU44b6SIvF8GrbLYple_1V9iinmH5-v-VUWUBg/formResponse")

time.sleep(3)

webdriver.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span").click()

all_questions: list[WebElement] = webdriver.get_elements_by_class("Qr7Oae")
for question in all_questions:

    time.sleep(1)

    child_elements = question.find_element(By.CSS_SELECTOR, '.aDTYNe.snByac.OvPDhc.OIC90c')
    print(child_elements)
    # answer_index = self.prior_result[self.prior_index][1]
    # 찾은 하위 요소들에 대해 원하는 작업을 수행합니다.
    if not child_elements:
        print('radio x')
    # child_elements[answer_index].click()
    # time.sleep(1)

time.sleep(10000)
# time.sleep(3)
# child_elements = webdriver.get_elements_by_css(None, '.aDTYNe.snByac.OvPDhc.OIC90c')
# print(child_elements)
