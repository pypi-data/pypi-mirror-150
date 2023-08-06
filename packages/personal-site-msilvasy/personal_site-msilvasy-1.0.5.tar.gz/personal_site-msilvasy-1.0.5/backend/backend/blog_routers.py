from rest_framework import routers

from backend.blog.views import PostViewSet

router = routers.DefaultRouter()
router.register('', PostViewSet)
