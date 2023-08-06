from rest_framework import routers

from backend.blog.views import CreatePostViewSet

router = routers.DefaultRouter()
router.register('', CreatePostViewSet)
