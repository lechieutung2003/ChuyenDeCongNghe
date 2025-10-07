from oauth.models.user import User
from hr.models.customer import Customer
from rest_framework import serializers

class FullUserSerializer(serializers.ModelSerializer):
    # Lấy thông tin từ bảng customer liên kết
    name = serializers.CharField(source='hr_customer.name', read_only=True)
    phone = serializers.CharField(source='hr_customer.phone', read_only=True)
    address = serializers.CharField(source='hr_customer.address', read_only=True)
    area = serializers.CharField(source='hr_customer.area', read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "name",
            "phone",
            "address",
            "area",
        ]