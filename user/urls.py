from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import SignUpView, UserListView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("signup/", SignUpView.as_view(), name="user-signup"),
    path("list/", UserListView.as_view(), name="user-list"),
]
