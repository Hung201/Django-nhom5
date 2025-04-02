from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, RegisterView, UserListView

# Khởi tạo router
router = DefaultRouter()
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('all-users', UserListView.as_view(), name='all-users'),  # API GET danh sách user
]
