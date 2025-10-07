from django.core.management.base import BaseCommand
from django.conf import settings
from oauth.models.user import User
from hr.models.customer import Customer

class Command(BaseCommand):
    help = 'Sync guest users from oauth_user to hr_customer'

    def handle(self, *args, **options):
        guests = User.objects.filter(is_guest=True)
        created_count = 0
        for user in guests:
            if not hasattr(user, 'hr_customer'):
                # Lấy tên ưu tiên: first_name + last_name hoặc email
                name = f"{user.first_name} {user.last_name}".strip() or user.email or str(user.id)
                Customer.objects.create(
                    user=user,
                    name=name,
                    phone=getattr(user, 'phone', ''),
                    email=user.email,
                    password=user.password,
                    address='',
                    area='urban',
                )
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Synced {created_count} guest users to hr_customer.'))
