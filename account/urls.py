from django.urls import path
from account import views

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name="register"),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateAccountAPIView.as_view(), name='activate'),
    path('resend-activation/', views.ResendActivationLinkAPIView.as_view(), name='resend-activation'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetAPIView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
