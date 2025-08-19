from django.urls import path
from . import views

urlpatterns = [
    path('all-entries/', views.all_entries),
    path('entries-by-blog-title/<str:title>/', views.entries_by_blog_title),
    path('blog-entries/<int:blog_id>/', views.blog_entries),
    path('entries-by-author/<str:author_name>/', views.entries_by_author),
    path('blogs-with-entry/', views.blogs_with_entry),
    path('entries-with-keyword/<str:keyword>/', views.entries_with_keyword),
    path('blog-entry-count/', views.blog_entry_count),
    path('entries-complex/<str:headline_keyword>/<str:blog_title>/', views.entries_complex),
    path('entries-with-authors/', views.entries_with_authors),
    path('author-entry-count/', views.author_entry_count),
]