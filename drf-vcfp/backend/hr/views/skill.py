from rest_framework import viewsets
from hr.models.skill import Skill
from hr.serializers.skill import SkillSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    required_alternate_scopes = {
        "list": [["admin:view"]],
        "retrieve": [["admin:view"]],
    }