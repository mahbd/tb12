from django.urls import path
from cf import views

urlpatterns = [
    path('last_sub_cf/', views.last_submission, name='find'),
]
