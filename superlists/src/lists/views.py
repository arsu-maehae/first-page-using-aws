from django.forms import ValidationError
from django.shortcuts import render
from django.shortcuts import render, redirect  # <--- เพิ่ม redirect
from lists.models import Item, List # <--- เพิ่ม List
def home_page(request):

    # ดึงข้อมูลทั้งหมดออกมา
    # items = Item.objects.all()
    # ส่งไปที่ template ในชื่อ 'items'
    # return render(request, "home.html", {"items": items})
    return render(request, "home.html")

def about_page(request):
    return render(request, 'about.html')

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    error = None # เตรียมตัวแปร error ไว้ก่อน

    # ถ้ามีการพิมพ์ส่งข้อมูล (POST) เข้ามาที่ URL นี้
    if request.method == 'POST':
        priority = request.POST.get('priority', 'medium')
        try:
            item = Item(text=request.POST["item_text"], list=our_list, priority=priority)
            item.full_clean()
            item.save()
            return redirect(f"/lists/{our_list.id}/")
        except ValidationError:
            # ถ้าเกิด Error ให้กำหนดข้อความ
            error = "You can't have an empty list item"

    # ถ้าเป็นแค่การเข้ามาดูเว็บปกติ (GET) หรือถ้าเกิด Error (POST แล้วพัง) ให้โชว์หน้านี้
    return render(request, "list.html", {"list": our_list, "error": error})


def new_list(request):
    nulist = List.objects.create()
    priority = request.POST.get('priority', 'medium')
    
    # 1. สร้าง Object ไว้ใน Memory ก่อน (ยังไม่เซฟลง DB)
    item = Item(
        text=request.POST["item_text"], 
        list=nulist,
        priority=priority 
    )
    
    try:
        item.full_clean()  # 2. ให้ Django ตรวจสอบว่าว่างไหม
        item.save()        # 3. ถ้าไม่ว่าง ค่อยเซฟลง DB
    except ValidationError:
        nulist.delete()    # 4. ถ้าว่าง (Error) ให้ลบ List ที่เผลอสร้างไปเมื่อกี้ทิ้ง
        error = "You can't have an empty list item"
        # 5. ส่งหน้าเว็บเดิมกลับไป พร้อมข้อความ Error
        return render(request, "home.html", {"error": error}) 
        
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    # รับค่า priority
    priority = request.POST.get('priority', 'medium')
    
    Item.objects.create(
        text=request.POST["item_text"], 
        list=our_list,
        priority=priority # <--- บันทึก Priority ลงไป
    )
    return redirect(f"/lists/{our_list.id}/")

def edit_item(request, list_id, item_id):
    # 1. ดึง Item ที่ต้องการแก้มาจาก Database
    item = Item.objects.get(id=item_id)
    
    # 2. ถ้ามีการกด Save (ส่งข้อมูลแบบ POST มา)
    if request.method == 'POST':
        new_text = request.POST.get('item_text') # รับค่าจากช่องกรอก
        item.text = new_text        # อัปเดตข้อความใน Object
        item.save()                 # บันทึกลง Database
        return redirect(f'/lists/{list_id}/') # เด้งกลับไปหน้า List เดิม
    
    # 3. ถ้าเพิ่งกดเข้ามา (GET) ให้ส่งไปหน้าฟอร์มแก้ไข
    return render(request, 'edit_item.html', {'item': item, 'list_id': list_id})


def landing_page(request):
    return render(request, 'landing.html')