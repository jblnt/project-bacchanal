from django.urls import path
from . import views
#from .views import ArticleDetailView

from datetime import datetime

urlpatterns = [
    path('', views.newsListView, name='news-home'),
    path('archive/', views.archiveListView, name='archive'),
    path('search/', views.SearchView, name='global-search'),
    path('search/<str:query>/<str:topic>/', views.SearchView_Filter, name='global-search-filter'),
    path('article/<int:pk>-<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),

    path('sources/<str:source>/', views.source, name='source'),
    path('sports/<path:source>/<str:topic>/', views.sportsListView, name='category-sports')
]
