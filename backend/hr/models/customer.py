from django.db import models
from base.models import TimeStampedModel


from django.conf import settings

class Customer(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hr_customer', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    AREA_CHOICES = [
        # Các quận
        ("Hải Châu", "Hải Châu"),
        ("Ngũ Hành Sơn", "Ngũ Hành Sơn"),
        ("Liên Chiểu", "Liên Chiểu"),
        ("Sơn Trà", "Sơn Trà"),
        ("Cẩm Lệ", "Cẩm Lệ"),
        ("Thanh Khê", "Thanh Khê"),
        # Các phường xã
        ("An Hải", "An Hải"),
        ("An Khê", "An Khê"),
        ("An Thắng", "An Thắng"),
        ("Avương", "Avương"),
        ("Bà Nà", "Bà Nà"),
        ("Bàn Thạch", "Bàn Thạch"),
        ("Bến Giằng", "Bến Giằng"),
        ("Bến Hiên", "Bến Hiên"),
        ("Chiên Đàn", "Chiên Đàn"),
        ("Đắc Pring", "Đắc Pring"),
        ("Đại Lộc", "Đại Lộc"),
        ("Điện Bàn", "Điện Bàn"),
        ("Điện Bàn Bắc", "Điện Bàn Bắc"),
        ("Điện Bàn Đông", "Điện Bàn Đông"),
        ("Điện Bàn Tây", "Điện Bàn Tây"),
        ("Đồng Dương", "Đồng Dương"),
        ("Đông Giang", "Đông Giang"),
        ("Đức Phú", "Đức Phú"),
        ("Duy Nghĩa", "Duy Nghĩa"),
        ("Duy Xuyên", "Duy Xuyên"),
        ("Gò Nổi", "Gò Nổi"),
        ("Hà Nha", "Hà Nha"),
        ("Hải Vân", "Hải Vân"),
        ("Hiệp Đức", "Hiệp Đức"),
        ("Hòa Cường", "Hòa Cường"),
        ("Hòa Khánh", "Hòa Khánh"),
        ("Hòa Tiến", "Hòa Tiến"),
        ("Hòa Vang", "Hòa Vang"),
        ("Hòa Xuân", "Hòa Xuân"),
        ("Hoàng Sa", "Hoàng Sa"),
        ("Hội An", "Hội An"),
        ("Hội An Đông", "Hội An Đông"),
        ("Hội An Tây", "Hội An Tây"),
        ("Hùng Sơn", "Hùng Sơn"),
        ("Hương Trà", "Hương Trà"),
        ("Khâm Đức", "Khâm Đức"),
        ("La Dêê", "La Dêê"),
        ("La Êê", "La Êê"),
        ("Lãnh Ngọc", "Lãnh Ngọc"),
        ("Nam Giang", "Nam Giang"),
        ("Nam Phước", "Nam Phước"),
        ("Nam Trà My", "Nam Trà My"),
        ("Nông Sơn", "Nông Sơn"),
        ("Núi Thành", "Núi Thành"),
        ("Phú Ninh", "Phú Ninh"),
        ("Phú Thuận", "Phú Thuận"),
        ("Phước Chánh", "Phước Chánh"),
        ("Phước Hiệp", "Phước Hiệp"),
        ("Phước Năng", "Phước Năng"),
        ("Phước Thành", "Phước Thành"),
        ("Phước Trà", "Phước Trà"),
        ("Quảng Phú", "Quảng Phú"),
        ("Quế Phước", "Quế Phước"),
        ("Quế Sơn", "Quế Sơn"),
        ("Quế Sơn Trung", "Quế Sơn Trung"),
        ("Sơn Cẩm Hà", "Sơn Cẩm Hà"),
        ("Sông Kôn", "Sông Kôn"),
        ("Sông Vàng", "Sông Vàng"),
        ("Tam Anh", "Tam Anh"),
        ("Tam Hải", "Tam Hải"),
        ("Tam Kỳ", "Tam Kỳ"),
        ("Tam Mỹ", "Tam Mỹ"),
        ("Tam Xuân", "Tam Xuân"),
        ("Tân Hiệp", "Tân Hiệp"),
        ("Tây Giang", "Tây Giang"),
        ("Tây Hồ", "Tây Hồ"),
        ("Thăng An", "Thăng An"),
        ("Thăng Bình", "Thăng Bình"),
        ("Thăng Điền", "Thăng Điền"),
        ("Thăng Phú", "Thăng Phú"),
        ("Thăng Trường", "Thăng Trường"),
        ("Thạnh Bình", "Thạnh Bình"),
        ("Thạnh Mỹ", "Thạnh Mỹ"),
        ("Thu Bồn", "Thu Bồn"),
        ("Thượng Đức", "Thượng Đức"),
        ("Tiên Phước", "Tiên Phước"),
        ("Trà Đốc", "Trà Đốc"),
        ("Trà Giáp", "Trà Giáp"),
        ("Trà Leng", "Trà Leng"),
        ("Trà Liên", "Trà Liên"),
        ("Trà Linh", "Trà Linh"),
        ("Trà My", "Trà My"),
        ("Trà Tân", "Trà Tân"),
        ("Trà Tập", "Trà Tập"),
        ("Trà Vân", "Trà Vân"),
        ("Việt An", "Việt An"),
        ("Vu Gia", "Vu Gia"),
        ("Xuân Phú", "Xuân Phú"),
    ]
    area = models.CharField(max_length=50, choices=AREA_CHOICES)  # Tăng độ dài để chứa tên phường dài

    class Meta:
        db_table = "hr_customer"

class ServiceType(TimeStampedModel):
    name = models.CharField(max_length=100)
    price_per_m2 = models.IntegerField()
    cleaning_rate_m2_per_h = models.IntegerField()

    class Meta:
        db_table = "hr_service_type"
