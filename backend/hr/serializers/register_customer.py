
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from hr.models.customer import Customer

User = get_user_model()

class RegisterCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    # name sẽ tự động được tạo từ first_name và last_name, không cần nhập từ frontend
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    area = serializers.ChoiceField(choices=Customer.AREA_CHOICES)

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        name = f"{first_name} {last_name}".strip()
        #user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            is_guest=True
        )
        user.is_guest = True
        user.save()
        validated_data['name'] = name
        # customer = Customer.objects.create(user=user, **validated_data)
        customer = Customer.objects.create(user=user, password=make_password(password), **validated_data)
        return customer

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "user": str(instance.user.id) if instance.user else None,
            "email": instance.user.email if instance.user else None,
            "first_name": instance.user.first_name if instance.user else None,
            "last_name": instance.user.last_name if instance.user else None,
            "name": instance.name,
            "phone": instance.phone,
            "address": instance.address,
            "area": instance.area
        }
