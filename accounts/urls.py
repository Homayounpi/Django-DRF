from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


app_name = 'accounts'


urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    # path('token-auth/', auth_token.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pire'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserApi.as_view()),
    path('users_list/', views.UserListApi.as_view()),

]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
urlpatterns += router.urls




