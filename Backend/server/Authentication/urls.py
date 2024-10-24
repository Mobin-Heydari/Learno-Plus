from django.urls import path
from . import views



app_name = "authentication"


urlpatterns = [
    # Tokens 
    path('token/', views.TokenObtainView.as_view(), name="token_obtain"),
]
