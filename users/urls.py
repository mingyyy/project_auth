from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.frontpage, name='frontpage'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('update/', views.update, name='update')
]