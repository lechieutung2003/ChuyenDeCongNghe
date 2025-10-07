from rest_framework import serializers
from rest_framework.fields import UUIDField
from rest_framework.exceptions import ValidationError
from datetime import datetime, time
from django.utils import timezone
import pytz
from base.serializers import WritableNestedSerializer
from ..models import Employee
from hr.models.skill import EmployeeSkill, Skill
from oauth.models import User, Role
from oauth.serializers import UserShortSerializer, RoleShortSerializer
from .employee_additional_information import EmployeeAdditionalInformationSerializer


class EmployeeSerializer(WritableNestedSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='user')
    office_id = UUIDField(required=False, allow_null=True)
    roles = RoleShortSerializer(many=True, required=False)
    role_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Role.objects.all(),
                                                   source='roles')
    additional_information = EmployeeAdditionalInformationSerializer(many=True, required=False)
    computed_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    skills = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of skill names to assign to the employee"
    )

    def get_skills(self, obj):
        return [es.skill.name for es in EmployeeSkill.objects.filter(employee=obj)]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Thêm skills từ hàm get_skills
        data['skills'] = self.get_skills(instance)
        return data

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'user_id',
            'office_id',
            'first_name',
            'last_name',
            'work_mail',
            'personal_mail',
            'date_of_birth',
            'join_date',
            'phone',
            'gender',
            'avatar',
            'roles',
            'role_ids',
            'additional_information',
            'status',  # This will be auto-updated
            'updated_at',
            # Working fields
            'area',
            'working_start_time',
            'working_end_time',
            'completed_orders_count',
            'salary',
            'total_hours_worked',
            'computed_status',
            'status_text',
            'skills',
        ]
        extra_kwargs = {
            'user': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'work_mail': {'required': False},
            'personal_mail': {'required': False},
            'date_of_birth': {'required': False},
            'phone': {'required': False},
            'gender': {'required': False},
            'avatar': {'required': False},
            'roles': {'required': False},
            'status': {'read_only': True},  # Auto-computed, read-only
            'updated_at': {'read_only': True},
            'area': {'required': False},
            'working_start_time': {'required': False},
            'working_end_time': {'required': False},
            'completed_orders_count': {'required': False},
            'salary': {'required': False},
            'total_hours_worked': {'required': False},
            'skills': {'required': False},
        }
        nested_create_fields = ["user"]
        nested_update_fields = ["additional_information"]
    
    def get_computed_status(self, obj):
        """Compute current status based on working hours"""
        return self._calculate_current_status(obj)['status_value']
    
    def get_status_text(self, obj):
        """Get human-readable status text"""
        return self._calculate_current_status(obj)['status_text']
    
    def _calculate_current_status(self, obj):
        """
        Calculate current status:
        - 0: No working hours set
        - 1: Active (current time within working hours)  
        - 2: Inactive (current time outside working hours)
        """
        try:
            # Nếu chưa set working hours
            if not obj.working_start_time or not obj.working_end_time:
                return {
                    'status_value': 0,
                    'status_text': 'No working hours set'
                }
            
            # Get current time in Vietnam timezone
            try:
                vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                current_time = timezone.now().astimezone(vietnam_tz).time()
            except Exception:
                current_time = timezone.now().time()
            
            start_time = obj.working_start_time
            end_time = obj.working_end_time
            
            # Check if current time is within working hours
            if start_time <= end_time:
                # Normal shift: same day
                is_within_hours = start_time <= current_time <= end_time
            else:
                # Overnight shift: crosses midnight
                is_within_hours = current_time >= start_time or current_time <= end_time
            
            if is_within_hours:
                return {
                    'status_value': 1,
                    'status_text': 'Active'
                }
            else:
                return {
                    'status_value': 2,
                    'status_text': 'Inactive'
                }
                
        except Exception as e:
            print(f"Error calculating status: {e}")
            return {
                'status_value': 0,
                'status_text': 'Status calculation error'
            }
    
    def update(self, instance, validated_data):
        """Override update to auto-calculate status"""
        # Lấy danh sách kỹ năng từ validated_data
        skills = validated_data.pop('skills', [])
        # Update instance với validated data
        updated_instance = super().update(instance, validated_data)
        
        # Gán kỹ năng mới
        self._assign_skills(updated_instance, skills)
        
        # Auto-calculate và update status
        status_info = self._calculate_current_status(updated_instance)
        updated_instance.status = status_info['status_value']
        updated_instance.save(update_fields=['status'])
        
        return updated_instance
    
    def create(self, validated_data):
        """Override create to auto-calculate status"""
        skills = validated_data.pop('skills', [])
        instance = super().create(validated_data)
        
        # Gán kỹ năng mới
        self._assign_skills(instance, skills)
        
        # Auto-calculate và set initial status
        status_info = self._calculate_current_status(instance)
        instance.status = status_info['status_value']
        instance.save(update_fields=['status'])
        
        return instance
    
    def _assign_skills(self, employee, skills):
        """
        Gán danh sách kỹ năng cho nhân viên.
        - Xóa các kỹ năng cũ không còn trong danh sách mới.
        - Thêm các kỹ năng mới.
        Raise ValidationError nếu có lỗi.
        """
        try:
            # Lấy các kỹ năng hiện tại của nhân viên
            current_skills = set(EmployeeSkill.objects.filter(employee=employee).values_list('skill__name', flat=True))
            new_skills = set(skills)
            print("current_skills", current_skills)
            print("new_skills", new_skills)

            # Xóa các kỹ năng không còn trong danh sách mới
            skills_to_remove = current_skills - new_skills
            print("skills_to_remove", skills_to_remove)
            deleted_count, _ = EmployeeSkill.objects.filter(employee=employee, skill__name__in=skills_to_remove).delete()
            if deleted_count < len(skills_to_remove):
                raise ValidationError(f"Failed to remove some skills for employee {employee.id}")

            # Thêm các kỹ năng mới
            for skill_name in new_skills - current_skills:
                try:
                    skill, created = Skill.objects.get_or_create(name=skill_name)
                    print(f"Assigning skill '{skill.name}' to employee {employee.id}")
                    EmployeeSkill.objects.create(employee=employee, skill=skill)
                    print(f"Successfully assigned skill '{skill.name}' to employee {employee.id}")
                except Exception as skill_error:
                    print(f"Error assigning skill '{skill_name}' to employee {employee.id}: {skill_error}")
                    raise ValidationError(f"Failed to assign skill '{skill_name}': {str(skill_error)}")

        except ValidationError:
            raise  # Re-raise ValidationError
        except Exception as e:
            print(f"Unexpected error in _assign_skills for employee {employee.id}: {e}")
            raise ValidationError(f"Unexpected error assigning skills: {str(e)}")


class EmployeeShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='user')
    computed_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'user_id',
            'office_id',
            'first_name',
            'last_name',
            'work_mail',
            'personal_mail',
            'date_of_birth',
            'phone',
            'gender',
            'avatar',
            'status',
            'area',
            'working_start_time',
            'working_end_time',
            'completed_orders_count',
            'salary',
            'total_hours_worked',
            'computed_status',
            'status_text'
        ]
        extra_kwargs = {
            'status': {'read_only': True},
            # ... other fields same as above
        }
    
    def get_computed_status(self, obj):
        """Reuse the same calculation logic"""
        serializer = EmployeeSerializer()
        return serializer._calculate_current_status(obj)['status_value']
    
    def get_status_text(self, obj):
        """Reuse the same calculation logic"""
        serializer = EmployeeSerializer()
        return serializer._calculate_current_status(obj)['status_text']