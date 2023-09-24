from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('api/chat/', views.chat_endpoint, name='chat_endpoint'),
    path('api/chat/history/', views.chat_history_endpoint, name='chat_history_endpoint'),
]
