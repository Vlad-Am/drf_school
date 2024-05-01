from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, UserCreateAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path("pays/", PaymentCreateAPIView.as_view(), name="pays"),

] + router.urls
