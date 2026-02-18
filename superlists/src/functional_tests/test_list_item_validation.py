from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # 1. Edith ไปที่หน้าแรก เข้าแอป To-Do List และเผลอกด Enter ช่องว่างๆ
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "To-Do List").click()
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        # 2. หน้าเว็บโหลดใหม่ และมีข้อความแจ้งเตือนสีแดง (class .invalid-feedback)
        # 🌟 สังเกตการใช้ฟังก์ชันวิเศษ wait_for() + lambda ที่เราเพิ่งสร้างครับ! 🌟
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        # 3. เธอเลยลองพิมพ์ข้อความปกติเข้าไป คราวนี้ผ่านใช้งานได้
        self.browser.find_element(By.ID, "id_new_item").send_keys("Buy milk")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # 4. ด้วยความดื้อ เธอตั้งใจลองกด Enter ส่งค่าว่างเข้าไปอีกรอบจากหน้า List
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        # 5. เธอได้รับคำเตือนเหมือนเดิมเป๊ะ
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        # 6. เธอแก้ไขให้ถูกต้องแล้วพิมพ์ข้อความเข้าไปใหม่
        self.browser.find_element(By.ID, "id_new_item").send_keys("Make tea")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")