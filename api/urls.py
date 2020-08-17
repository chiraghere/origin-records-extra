from django.urls import path
from . import views
from rest_framework.authtoken import views as tokenviews

urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='create-user'),
    path('loginuser/', views.Userlogin.as_view(), name='login-user'),
    path('get-token/', tokenviews.obtain_auth_token, name='get-token'),
    path('createnode/', views.PersonView.as_view(), name='create-node'),
    path('createrelation/', views.RelationView.as_view(), name='create-related-node')
]