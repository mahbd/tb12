from django.urls import path
from cf import views

urlpatterns = [
    path('', views.test, name='find'),
]
