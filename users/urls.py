from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='index.html'), name="logout"),
    path('frontpage/', views.frontpage, name='frontpage'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
]