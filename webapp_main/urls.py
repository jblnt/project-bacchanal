from django.urls import path
from . import views
from datetime import datetime

urlpatterns = [
    path('', views.newsListView, name='news-home'),
    path('archive/', views.archiveListView, name='archive'),
    path('article/<int:pk>-<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('search/', views.SearchView, name='global-search'),
    path('source/<str:source>/', views.source, name='source'),
    path('tags/', views.tagView, name='tags')
]
