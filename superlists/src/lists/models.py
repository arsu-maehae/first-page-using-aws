from django.db import models
from django.urls import reverse

class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

class Item(models.Model):
    text = models.TextField(default='')  # ข้อความของรายการ
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE) # รายการที่รายการนี้เป็นของ
    priority = models.TextField(max_length=10, default='medium')  # ความสำคัญของรายการ
    #priority = models.CharField(max_length=10, default='medium')  # ความสำคัญของรายการ
    
    # --- เพิ่มส่วนนี้ครับ ---
    #PRIORITY_CHOICES = [('high', 'High'),('medium', 'Medium'),('low', 'Low'),]
    #priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    # --------------------