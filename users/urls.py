from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('check-email/', views.check_email),
    path('google-signin/', views.google_signin),
    path('users/', views.user_list),
    path('users/<int:id>/', views.user_detail),
    path('forgot-password', views.forgot_password),
]
