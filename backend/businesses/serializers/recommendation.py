from rest_framework import serializers
from businesses.models import Employee
from hr.models import Order, Customer, Skill, EmployeeSkill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class RecommendationEmployeeSerializer(serializers.ModelSerializer):
    # Thêm trường skills như một SerializerMethodField
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 
            'first_name', 
            'last_name',
            'area',
            'skills',  # Trường tự định nghĩa, không phải từ model
            'total_hours_worked',
            'completed_orders_count',
            'salary',
        ]

    def get_skills(self, obj):
        """Lấy danh sách kỹ năng của nhân viên từ bảng liên kết"""
        # Lấy các bản ghi EmployeeSkill liên quan đến nhân viên này
        employee_skills = EmployeeSkill.objects.filter(employee=obj)
        # Trả về danh sách tên kỹ năng
        return [es.skill.name for es in employee_skills]

class RecommendationSerializer(serializers.Serializer):
    employee = RecommendationEmployeeSerializer()
    score = serializers.IntegerField()
    reasons = serializers.ListField(child=serializers.CharField())