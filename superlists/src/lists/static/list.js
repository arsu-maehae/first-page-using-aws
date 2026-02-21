let inputElement = document.getElementById('id_new_item');
let form = document.querySelector('form');
let table = document.getElementById('id_list_table');

// 1. ถ้ามีการพิมพ์ข้อความใหม่ ให้ซ่อนกล่อง Error ทันที
if (inputElement) {
    inputElement.addEventListener('keypress', function () {
        let errorElement = document.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.classList.remove('d-block');
            errorElement.style.display = 'none';
        }
    });
}

// 2. ดักจับตอนกด Enter (Submit ฟอร์ม)
if (form && table) {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // เบรก! ห้ามบราวเซอร์รีเฟรช

        let errorElement = document.querySelector('.invalid-feedback');
        let itemText = inputElement.value.trim();
        
        // --- เช็คช่องว่าง (ด่าทันทีไม่ต้องรอเซิร์ฟเวอร์) ---
        if (itemText === '') {
            if (errorElement) {
                errorElement.textContent = "You can't have an empty list item";
                errorElement.classList.add('d-block');
                errorElement.style.display = 'block'; 
            }
            return; // สั่งหยุด ไม่ต้องทำโค้ดบรรทัดล่างต่อ
        }

        // --- แอบส่งข้อมูลผ่าน Fetch API ---
        let formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // บอก Django ว่านี่คือ AJAX
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // คำนวณเลขลำดับ และจัดการสี Priority
                let rowCount = table.getElementsByTagName('tr').length + 1;
                let badgeClass = data.priority === 'high' ? 'bg-danger' : (data.priority === 'medium' ? 'bg-warning text-dark' : 'bg-success');
                let priorityText = data.priority.charAt(0).toUpperCase() + data.priority.slice(1);
                
                // สร้าง HTML แถวใหม่
                let newRow = `
                  <tr>
                    <td>
                        ${rowCount}: ${data.item_text}
                        <span class="badge ${badgeClass}">${priorityText}</span>
                    </td>
                    <td>
                        <a href="/lists/${data.list_id}/items/${data.item_id}/edit/">
                            <button>Edit</button>
                        </a>
                    </td>
                  </tr>
                `;
                
                // แปะลงตาราง และล้างช่อง Input ให้ว่าง
                table.innerHTML += newRow;
                inputElement.value = ''; 
                
            } else if (data.status === 'error') {
                // ถ้ามี Error ตอบกลับจากเซิร์ฟเวอร์
                if (errorElement) {
                    errorElement.textContent = data.error;
                    errorElement.classList.add('d-block');
                    errorElement.style.display = 'block';
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
}