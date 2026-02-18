from selenium.webdriver.common.by import By
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith ไปที่หน้าแรก
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # ต้องกดปุ่ม To-Do List ก่อน ถึงจะเจอ inputbox
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "To-Do List").click()

        # เธอสังเกตเห็นว่ากล่อง input จัดวางอยู่อย่างสวยงามตรงกลาง
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=80,
        )