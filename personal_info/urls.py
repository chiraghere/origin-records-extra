from django.urls import path
from . import views

urlpatterns = [
    path('tree/', views.Show_Relations.as_view(), name='Show_relations'),
    path('find/', views.Search.as_view(), name='Find'),
]