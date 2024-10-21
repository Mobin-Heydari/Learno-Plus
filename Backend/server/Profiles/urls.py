from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name = "Profiles"


urlpatterns = [
    
]



# Routers
router = DefaultRouter()
# ProfileViewSet router
router.register(r'', views.UserProfileViewSet, basename='profiles')
# Complaining the routers
urlpatterns += router.urls
