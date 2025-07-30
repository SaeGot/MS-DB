from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('member/<int:pk>/', views.search_view, name='member_detail'),
    path('play/<int:pk>/', views.search_view, name='play_detail'),
    path('version/', views.version, name='version'),
]