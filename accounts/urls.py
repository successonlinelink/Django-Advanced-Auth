from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  
    path("profile/", views.update_profile, name="update_profile"),  

    path("password/", views.change_password, name="change_password"),  


]