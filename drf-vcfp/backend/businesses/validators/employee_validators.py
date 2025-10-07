from rest_framework import serializers
from django.utils.translation import gettext as _
import re
from datetime import time, date


def validate_phone_number(value):
    """Validate Vietnamese phone number format"""
    if not value:
        return value
    
    # Remove spaces and special characters
    phone = re.sub(r'[\s\-\(\)]', '', str(value))
    
    # Vietnamese phone patterns
    phone_patterns = [
        r'^(\+84|84)[3|5|7|8|9][0-9]{8}$',  # +84 or 84 prefix
        r'^0[3|5|7|8|9][0-9]{8}$',          # 0 prefix
    ]
    
    is_valid = any(re.match(pattern, phone) for pattern in phone_patterns)
    
    if not is_valid:
        raise serializers.ValidationError(
            _("Phone number must be in Vietnamese format (e.g., 0901234567 or +84901234567)")
        )
    
    return value


def validate_working_hours(value):
    """Validate working hours are reasonable (5AM - 11:59PM)"""
    if not value:
        return value
    
    # Convert time to minutes for easier comparison
    total_minutes = value.hour * 60 + value.minute
    
    # Working hours should be between 5:00 AM and 11:59 PM
    min_time = 5 * 60      # 5:00 AM = 300 minutes
    max_time = 23 * 60 + 59  # 11:59 PM = 1439 minutes
    
    if total_minutes < min_time or total_minutes > max_time:
        raise serializers.ValidationError(
            _("Working hours must be between 5:00 AM and 11:59 PM")
        )
    
    return value


def validate_salary_amount(value):
    """Validate salary is within reasonable range"""
    if value is None:
        return value
        
    if value < 0:
        raise serializers.ValidationError(_("Salary cannot be negative"))
    
    if value < 1000000:  # 1 million VND minimum
        raise serializers.ValidationError(_("Salary must be at least 1,000,000 VND"))
    
    if value > 1000000000:  # 1 billion VND maximum
        raise serializers.ValidationError(_("Salary cannot exceed 1,000,000,000 VND"))
    
    return value


def validate_employee_name(value):
    """Validate employee first/last name"""
    if not value:
        return value
    
    # Remove extra whitespace
    name = value.strip()
    
    if len(name) < 1:
        raise serializers.ValidationError(_("Name cannot be empty"))
    
    if len(name) > 50:
        raise serializers.ValidationError(_("Name cannot exceed 50 characters"))
    
    # Check for valid characters (Vietnamese + English)
    if not re.match(r'^[a-zA-ZÀ-ỹ\s]+$', name):
        raise serializers.ValidationError(_("Name can only contain letters and spaces"))
    
    return name


def validate_work_area(value):
    """Validate work area"""
    if not value:
        return value
    
    area = value.strip()
    
    if len(area) < 2:
        raise serializers.ValidationError(_("Work area must be at least 2 characters"))
    
    if len(area) > 100:
        raise serializers.ValidationError(_("Work area cannot exceed 100 characters"))
    
    return area


class WorkingHoursValidator:
    """
    Validate that working hours are consistent:
    - Both start and end time must be provided together
    - End time should not be same as start time
    """
    
    def __init__(self, start_field='working_start_time', end_field='working_end_time'):
        self.start_field = start_field
        self.end_field = end_field
    
    def __call__(self, attrs):
        start_time = attrs.get(self.start_field)
        end_time = attrs.get(self.end_field)
        
        # Both must be provided together or both None
        if bool(start_time) != bool(end_time):
            raise serializers.ValidationError({
                'working_hours': _("Both start time and end time must be provided together")
            })
        
        # If both provided, validate they're not the same
        if start_time and end_time and start_time == end_time:
            raise serializers.ValidationError({
                self.end_field: _("End time cannot be the same as start time")
            })
        
        return attrs


class SkillsValidator:
    """Validate employee skills list"""
    
    def __init__(self, max_skills=10):
        self.max_skills = max_skills
    
    def __call__(self, value):
        if not value:
            return value
            
        if not isinstance(value, list):
            raise serializers.ValidationError(_("Skills must be a list"))
        
        if len(value) > self.max_skills:
            raise serializers.ValidationError(
                _("Employee cannot have more than {} skills").format(self.max_skills)
            )
        
        # Check for duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError(_("Duplicate skills are not allowed"))
        
        # Validate each skill name
        for skill in value:
            if not isinstance(skill, str):
                raise serializers.ValidationError(_("Each skill must be a string"))
            
            skill_name = skill.strip()
            if len(skill_name) < 2:
                raise serializers.ValidationError(_("Skill name must be at least 2 characters"))
            
            if len(skill_name) > 50:
                raise serializers.ValidationError(_("Skill name cannot exceed 50 characters"))
        
        return value


class AgeValidator:
    """Validate employee age based on date of birth"""
    
    def __init__(self, min_age=16, max_age=70):
        self.min_age = min_age
        self.max_age = max_age
    
    def __call__(self, value):
        if not value:
            return value
            
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < self.min_age:
            raise serializers.ValidationError(
                _("Employee must be at least {} years old").format(self.min_age)
            )
        
        if age > self.max_age:
            raise serializers.ValidationError(
                _("Employee cannot be older than {} years").format(self.max_age)
            )
        
        return value


class JoinDateValidator:
    """Validate employee join date"""
    
    def __call__(self, attrs):
        join_date = attrs.get('join_date')
        date_of_birth = attrs.get('date_of_birth')
        
        if not join_date or not date_of_birth:
            return attrs
        
        # Calculate age at join date
        age_at_join = join_date.year - date_of_birth.year - (
            (join_date.month, join_date.day) < (date_of_birth.month, date_of_birth.day)
        )
        
        if age_at_join < 16:
            raise serializers.ValidationError({
                'join_date': _("Employee must be at least 16 years old when joining")
            })
        
        # Join date cannot be in the future
        if join_date > date.today():
            raise serializers.ValidationError({
                'join_date': _("Join date cannot be in the future")
            })
        
        return attrs


class EmailDomainValidator:
    """Validate email domain for work emails"""
    
    def __init__(self, allowed_domains=None):
        self.allowed_domains = allowed_domains or []
    
    def __call__(self, value):
        if not value or not self.allowed_domains:
            return value
        
        domain = value.split('@')[1] if '@' in value else ''
        
        if domain and self.allowed_domains and domain not in self.allowed_domains:
            raise serializers.ValidationError(
                _("Email domain must be one of: {}").format(', '.join(self.allowed_domains))
            )
        
        return value


# Context-aware validator example
class UniqueWorkEmailValidator:
    """
    Validate work email is unique, excluding current instance during updates
    """
    requires_context = True
    
    def __call__(self, value, serializer_field):
        from ..models import Employee
        
        if not value:
            return value
        
        # Get current instance from serializer context
        serializer = serializer_field.parent
        current_instance = getattr(serializer, 'instance', None)
        
        # Check for existing employees with this email
        queryset = Employee.objects.filter(work_mail=value)
        
        # Exclude current instance during updates
        if current_instance:
            queryset = queryset.exclude(pk=current_instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                _("An employee with this work email already exists")
            )
        
        return value