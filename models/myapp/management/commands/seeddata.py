from django.core.management.base import BaseCommand
from myapp.models import Author, Profile, Blog, Entry

class Command(BaseCommand):
    help = "Seed initial data for myapp models"

    def handle(self, *args, **options):
        author = Author.objects.create(name="Nguyen Van A", email="a@example.com")
        Profile.objects.create(user=author, bio="Bio của A")
        blog = Blog.objects.create(title="Blog đầu tiên")
        entry = Entry.objects.create(blog=blog, headline="Bài viết 1", body_text="Nội dung bài viết")
        entry.authors.add(author)
        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))