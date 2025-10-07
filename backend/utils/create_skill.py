import os
import sys
import django

# Cấu hình Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from hr.models.skill import Skill
from django.db import transaction

# Danh sách kỹ năng mẫu
SKILL_NAMES = [
    "Regular Skill",
    "Deep Skill",
]

def create_skills():
    """
    Tạo các kỹ năng mẫu nếu chưa tồn tại.
    """
    print("Bắt đầu tạo kỹ năng...")
    skills_created = 0
    with transaction.atomic():
        for name in SKILL_NAMES:
            skill, created = Skill.objects.get_or_create(name=name)
            if created:
                skills_created += 1
                print(f"Đã thêm kỹ năng: {skill.name}")
            else:
                print(f"Kỹ năng đã tồn tại: {skill.name}")
    print(f"Đã tạo xong {skills_created} kỹ năng mới.")

def clear_skills():
    """
    Xóa tất cả các kỹ năng hiện có.
    """
    print("Xóa tất cả các kỹ năng...")
    deleted_count, _ = Skill.objects.all().delete()
    print(f"Đã xóa {deleted_count} kỹ năng.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tạo hoặc xóa dữ liệu kỹ năng")
    parser.add_argument("--clear", action="store_true", help="Xóa tất cả các kỹ năng trước khi tạo mới")
    
    args = parser.parse_args()

    if args.clear:
        clear_skills()

    create_skills()
    print("Hoàn thành quá trình tạo kỹ năng!")