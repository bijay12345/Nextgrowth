from . import views
from django.urls import path

urlpatterns = [
    path("register/", views.CustomUserCreate.as_view(), name="register-user"),
    path('user/login/',views.LoginAPIView.as_view(),name="user-login"),
    path('user/logout/',views.logout_view,name="user-logout"),
]