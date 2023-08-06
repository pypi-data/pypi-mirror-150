from rest_framework import routers

from .views import ChangePasswordViewSet

router = routers.DefaultRouter()
router.register('', ChangePasswordViewSet)
