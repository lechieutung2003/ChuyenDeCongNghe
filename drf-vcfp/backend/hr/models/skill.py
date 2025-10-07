from django.db import models
from base.models import TimeStampedModel

class Skill(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "hr_skill"

    def __str__(self):
        return self.name
    
class EmployeeSkill(TimeStampedModel):
    employee = models.ForeignKey('businesses.Employee', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_employee_skill"
        unique_together = ("employee", "skill")
    
    def __str__(self):
        return f"{self.employee.first_name} - {self.skill.name}"
