from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views



app_name = "authentication"


urlpatterns = [
    # Tokens 
    path('token/', views.TokenObtainView.as_view(), name="token_obtain"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    
    # Login
    path('login/', views.UserLoginView.as_view(), name="user_login"),
    #  Register
    path('register/<str:token>/', views.UserRegisterView.as_view(), name="user_register"),
    # OTP 
    path('one-time-pass/', views.OneTimePasswordView.as_view(), name="one_time_password"),
]
