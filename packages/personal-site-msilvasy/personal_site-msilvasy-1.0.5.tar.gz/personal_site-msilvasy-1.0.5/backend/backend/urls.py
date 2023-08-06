"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import users_routers, password_routers, blog_routers, create_blog_routers, message_routers
from .views import UserRetrieveUpdateDestroyAPIView, PasswordTokenCheckGenericAPIView, RequestPasswordResetGenericAPIView, SetNewPasswordGenericAPIView
from backend.blog.views import LoginGenericAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djoser.urls.authtoken')),
    path('users/', include(users_routers.router.urls)),
    path('change_password/', include(password_routers.router.urls)),
    path('blog_posts/', include(blog_routers.router.urls)),
    path('create_blog_post/', include(create_blog_routers.router.urls)),
    path('messages/',include(message_routers.router.urls)),
    path('data/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-data'),
    path('reset_password/<uidb64>/<token>/', PasswordTokenCheckGenericAPIView.as_view(), name='reset-password'),
    path('request_password_reset/', RequestPasswordResetGenericAPIView.as_view(), name='request-password-reset'),
    path('password_reset_complete/', SetNewPasswordGenericAPIView.as_view(), name='password-reset-complete'),
    path('user_logins/', LoginGenericAPIView.as_view(), name='user-logins')
]
