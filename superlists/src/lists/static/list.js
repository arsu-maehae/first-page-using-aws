// ไฟล์: src/lists/static/list.js

let inputElement = document.getElementById('id_new_item');

inputElement.addEventListener('keypress', function () {
    let errorElement = document.querySelector('.invalid-feedback');
    
    if (errorElement) {
        errorElement.classList.remove('d-block');
        errorElement.style.display = 'none';
    }
});