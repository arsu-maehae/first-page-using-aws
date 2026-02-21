from django.test import TestCase
from lists.models import Item, List
from django.utils import html

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        # แก้ 1: เปลี่ยนจาก "/" เป็น "/lists/"
        response = self.client.get("/lists/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self):
        # แก้ 2: เปลี่ยนจาก "/" เป็น "/lists/"
        response = self.client.get("/lists/")
        self.assertContains(response, '<form method="POST" action="/lists/new">')
        # แก้ 3: เช็คแค่ attribute เพื่อไม่ให้พังเวลาเราเปลี่ยน CSS class
        self.assertContains(response, 'name="item_text"')
        self.assertContains(response, 'id="id_new_item"')
    
    def test_only_saves_items_when_necessary(self):
        # แก้ 4: เปลี่ยนจาก "/" เป็น "/lists/"
        self.client.get("/lists/")
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        
        # 🟢 แก้ไข: ใช้ html.escape() ป้องกันเครื่องหมาย '
        expected_error = html.escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    # 🟢 เพิ่มเทสต์นี้เข้าไปใหม่ (เช็คว่าถ้าค่าว่าง ห้ามเซฟลง DB เด็ดขาด)
    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)



class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")  
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        
        # 🟢 แก้ไข: ลบ /add_item ออกไปเลย
        self.assertContains(
            response,
            f'<form method="POST" action="/lists/{mylist.id}/">',
        )
        self.assertContains(response, 'name="item_text"')
        self.assertContains(response, 'id="id_new_item"')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()  
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()  
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")  

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    # 🟢 ย้าย 2 ฟังก์ชันนี้มาจาก NewItemTest และลบ /add_item ออกจาก URL
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/", # ลบ add_item
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/", # ลบ add_item
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

        # 🚨 อย่าลืมลบคลาส NewItemTest ด้านล่างสุดทิ้งด้วยนะครับ!