from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class Profile(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE)
    bio = models.TextField()

class Blog(models.Model):
    title = models.CharField(max_length=100)

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    authors = models.ManyToManyField(Author)
