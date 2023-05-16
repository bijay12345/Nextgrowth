from django.urls import path
from . import views

urlpatterns = [
    path("",views.AppView.as_view(),name="applications"),
    path("app/<int:id>/",views.AppView.as_view(),name="detail"),
    # path("register/",views.RegisterView.as_view(),name="register"),
    path("profile/<int:id>/",views.ProfileView.as_view(),name="profile"),
    path("user/photo/",views.TaskUploadView.as_view(),name="user-upload"),
    path("points/<int:user_id>/",views.UserPointsView.as_view(),name="points"),
    path("user/task/",views.UserTaskView.as_view(),name="user-tasks"),

    # ADMIN URLS 
    path("admin-panel/",views.AdminPanel.as_view(),name="admin-panel"),
]