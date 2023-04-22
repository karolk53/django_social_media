from django.urls import path
from .views import signup_view

app_name = "register"

urlpatterns = [
    path("",signup_view,name="register")
]