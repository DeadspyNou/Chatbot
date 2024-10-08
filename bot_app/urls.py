from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'ajax_part/', views.ajax_part, name='ajax_part'),
]