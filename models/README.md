## Hướng dẫn sử dụng và phát triển dự án

---

### 1. Khởi tạo dự án

- Tạo môi trường ảo:
  ```sh
  python -m venv venv
  ```
- Kích hoạt môi trường ảo:
    ```sh
    venv\Scripts\activate
    ```
- Cài đặt Django và các thư viện cần thiết:
  ```sh
  pip install -r requirements.txt
  ```

---

### 2. Cấu trúc thư mục

```
ChuyenDeCongNghe/
│   └── models/
│       └── myapp/
│           ├── models/
│           │   ├── author.py
│           │   ├── blog.py
│           │   ├── entry.py
│           │   ├── profile.py
│           │   └── __init__.py
│           ├── migrations/
│           ├── views.py
│           ├── urls.py
│           ├── tests.py
│           └── management/
│               └── commands/
│                   └── seeddata.py
├── requirements.txt
└── README.md
```

---

### 3. Tạo models và migrations

- Viết models vào các file trong `myapp/models/`.
- Tạo migration:
  ```sh
  python manage.py makemigrations myapp
  ```
- Áp dụng migration:
  ```sh
  python manage.py migrate
  ```

---

### 4. Seed dữ liệu mẫu

- Viết lệnh seed trong `management/commands/seeddata.py`.
- Chạy lệnh seed:
  ```sh
  python manage.py seeddata
  ```

---

### 5. Viết queries và views

- Viết các hàm truy vấn (relationship & complex queries) trong `views.py`.
- Khai báo các endpoint trong `urls.py`.

---

### 6. Kiểm tra queries

- Chạy server:
  ```sh
  python manage.py runserver
  ```
- Truy cập các endpoint qua trình duyệt hoặc Postman để kiểm tra kết quả.

---

### 7. Quản lý migration

- Tạo migration mới khi thay đổi models:
  ```sh
  python manage.py makemigrations myapp
  ```
- Áp dụng migration:
  ```sh
  python manage.py migrate myapp
  ```
- Rollback migration:
  ```sh
  python manage.py migrate myapp <migration_name>
  ```
- Tạo migration rỗng:
  ```sh
  python manage.py makemigrations --empty myapp
  ```
- Xem trạng thái migration:
  ```sh
  python manage.py showmigrations myapp
  ```
- Để xem các câu lệnh SQL mà migration sẽ thực thi:
  ```sh
  python manage.py sqlmigrate myapp <migration_name>
  ```
  
---

### 8. Tạo requirements.txt

- Lưu lại các thư viện đã cài:
  ```sh
  pip freeze > requirements.txt
  ```
