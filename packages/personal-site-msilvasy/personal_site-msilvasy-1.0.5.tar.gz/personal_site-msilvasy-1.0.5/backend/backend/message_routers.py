from rest_framework import routers

from backend.blog.views import AlertMessageViewSet

router = routers.DefaultRouter()
router.register('', AlertMessageViewSet)
