from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Edith ไปที่หน้า homepage
        self.browser.get(self.live_server_url)

        # ต้องคลิกเข้า To-Do List ก่อน
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "To-Do List").click()

        # เช็คว่าเข้ามาถูกหน้า (Title มีคำว่า To-Do)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # เธอพิมพ์ "Buy peacock feathers"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')

        # เธอกด Enter
        inputbox.send_keys(Keys.ENTER)
        
        # เช็คตาราง
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # เธอพิมพ์รายการที่ 2
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # เช็คตารางอีกรอบ
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith เริ่ม list ใหม่
        self.browser.get(self.live_server_url)
        
        # คลิกเข้า App ก่อน
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "To-Do List").click()
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Francis ผู้ใช้ใหม่เข้ามา
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis เข้ามาหน้าแรก
        self.browser.get(self.live_server_url)
        
        # Francis ก็ต้องคลิกเข้า App เหมือนกัน
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "To-Do List").click()

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)