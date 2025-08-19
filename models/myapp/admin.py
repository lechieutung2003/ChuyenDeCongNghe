from django.contrib import admin
from myapp.models import Author, Profile, Blog, Entry

admin.site.register(Author)
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Entry)