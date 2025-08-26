## Giới thiệu
Đây là dự án mẫu Django dùng để quản lý và ghi lại các log message do người dùng nhập vào.

## Yêu cầu hệ thống
- Python 3.10 trở lên
- pip
- Git

## Các bước thực hiện

### 1. Clone dự án
```sh
git clone <repo-url>
cd view_layer
```

### 2. Tạo môi trường ảo và cài đặt package
```sh
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. Khởi tạo database
```sh
python manage.py migrate
```

### 4. Chạy server phát triển
```sh
python manage.py runserver
```
Truy cập [http://127.0.0.1:8000/] trên trình duyệt.

### 5. Các chức năng chính
- **Trang chủ:** Hiển thị danh sách các log message mới nhất.
- **Thêm log:** Nhấn "Add Log Message" để ghi lại thông điệp mới.
- **Trang giới thiệu:** Xem thông tin về ứng dụng.
- **Xem thời gian hiện tại:** Truy cập `/now/` để xem thời gian hệ thống.

### 6. Cấu trúc thư mục
- `manage.py`: File quản lý dự án Django.
- `web_django/`: Cấu hình dự án.
- `myapp/`: Ứng dụng chính, chứa models, views, forms, templates.
- `requirements.txt`: Danh sách package cần thiết.
- `db.sqlite3`: Database SQLite.

### 7. Tùy chỉnh
- Thay đổi giao diện bằng cách chỉnh sửa các file trong `myapp/templates/hello/`.
- Thêm chức năng mới bằng cách bổ sung view và url trong `myapp/views.py` và `myapp/urls.py`.

---

## Tài liệu tham khảo
- [Django Documentation](https://docs.djangoproject.com/en/5.0/)