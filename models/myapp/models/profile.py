from django.db import models
from .author import Author

class Profile(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE)
    bio = models.TextField()