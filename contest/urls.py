from django.urls import path

from contest import views

urlpatterns = [
    path('', views.test, name='test'),
]
