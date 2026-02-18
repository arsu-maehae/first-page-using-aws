from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base import FunctionalTest

class CalculatorTest(FunctionalTest):

    def test_can_navigate_to_calculator_and_calculate_django(self):
        # 1. Edith เข้ามาที่หน้าแรก (Home)
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 2. เธอเห็นปุ่มไป Calculator และกดมัน
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "Calculator").click()

        # 3. ตอนนี้เธออยู่ที่หน้าเลือกโหมด เธอเลือก "Django Style"
        try:
            self.browser.find_element(By.CSS_SELECTOR, "a[href='/calc/django/']").click()
        except:
            self.browser.find_element(By.PARTIAL_LINK_TEXT, "Django").click()

        # 4. เธอเจอฟอร์มเครื่องคิดเลข และลองกรอกเลข
        num1_box = self.browser.find_element(By.NAME, 'num1')
        num1_box.send_keys('10')

        num2_box = self.browser.find_element(By.NAME, 'num2')
        num2_box.send_keys('5')

        operator_box = self.browser.find_element(By.NAME, 'operator')
        Select(operator_box).select_by_value('add') 

        submit_button = self.browser.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('15.0', body_text)

    def test_can_use_js_calculator(self):
        # เข้าไปที่หน้า JS โดยตรง
        self.browser.get(self.live_server_url + "/calc/js/")

        self.browser.find_element(By.ID, 'num1').send_keys('8')
        self.browser.find_element(By.ID, 'num2').send_keys('8')
        
        select = Select(self.browser.find_element(By.ID, 'operator'))
        select.select_by_value('multiply')

        self.browser.find_element(By.TAG_NAME, 'button').click()

        result_span = self.browser.find_element(By.ID, 'result')
        self.assertEqual(result_span.text, '64')

    def test_division_by_zero(self):
        # --- 1. ทดสอบโหมด Django (Server-Side) ---
        self.browser.get(self.live_server_url + "/calc/django/")
        self.browser.find_element(By.NAME, 'num1').send_keys('10')
        self.browser.find_element(By.NAME, 'num2').send_keys('0')
        
        operator_box = self.browser.find_element(By.NAME, 'operator')
        Select(operator_box).select_by_value('divide')
        
        self.browser.find_element(By.TAG_NAME, 'button').click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn("หาค่าไม่ได้ (หารด้วยศูนย์)", body_text) 

        # --- 2. ทดสอบโหมด JavaScript (Client-Side) ---
        self.browser.get(self.live_server_url + "/calc/js/")
        self.browser.find_element(By.ID, 'num1').send_keys('7')
        self.browser.find_element(By.ID, 'num2').send_keys('0')
        
        operator_box = self.browser.find_element(By.ID, 'operator')
        Select(operator_box).select_by_value('divide')
        
        self.browser.find_element(By.TAG_NAME, 'button').click()

        result_span = self.browser.find_element(By.ID, 'result')
        self.assertIn("Error", result_span.text)