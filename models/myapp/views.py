from django.shortcuts import render
from django.http import JsonResponse
from .models import Author, Blog, Entry
from django.db.models import Count
from django.db.models import Q

def all_entries(request):
    entries = Entry.objects.all()
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def entries_by_blog_title(request, title):
    entries = Entry.objects.filter(blog__title=title)
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def blog_entries(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    entries = blog.entry_set.all()
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def entries_by_author(request, author_name):
    entries = Entry.objects.filter(authors__name=author_name)
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def blogs_with_entry(request):
    blogs = Blog.objects.filter(entry__isnull=False).distinct()
    return JsonResponse({'blogs': [b.title for b in blogs], 'count': blogs.count()})

def entries_with_keyword(request, keyword):
    entries = Entry.objects.filter(headline__icontains=keyword)
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def blog_entry_count(request):
    blogs = Blog.objects.annotate(entry_count=Count("entry"))
    return JsonResponse({'counts': {b.title: b.entry_count for b in blogs}})

def entries_complex(request, headline_keyword, blog_title):
    entries = Entry.objects.filter(
        Q(headline__icontains=headline_keyword) | Q(blog__title=blog_title)
    )
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

def entries_with_authors(request):
    entries = Entry.objects.filter(authors__isnull=False).distinct()
    return JsonResponse({'entries': [e.headline for e in entries], 'count': entries.count()})

from django.db.models import Count

def author_entry_count(request):
    authors = Author.objects.annotate(entry_count=Count("entry"))
    return JsonResponse({'counts': {a.name: a.entry_count for a in authors}})