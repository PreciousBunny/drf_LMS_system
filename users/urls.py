from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import *
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
    path('users', UserListAPIView.as_view(), name='user_list'),
    path('users/detail/<int:pk>', UserRetrieveAPIView.as_view(), name='users_detail'),
    path('users/create', UserCreateAPIView.as_view(), name='user_create'),
    path('users/update/<int:pk>', UserUpdateAPIView.as_view(), name='user_update'),

    # Authorization Token
    path('login/', views.obtain_auth_token, name='user_login'),
    path('logout/', Logout.as_view(), name='user_logout'),

    # Authorization JWT Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]