from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .serializers import PostSerializer, LoginSerializer, AlertMessageSerializer
from .models import Post, Login, AlertMessage

class PostViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    permission_classes = []
    queryset = Post.objects.all()

    def list(self, request):
        page = int(request.query_params.get('page'))
        searchInput = request.query_params.get('searchInput')
        order = request.query_params.get('order')
        num_posts = 5
        self.queryset = Post.objects.filter(
            Q(name__icontains=searchInput) |
            Q(title__icontains=searchInput)
        )
        total = len(self.queryset)
        start = (page - 1) * num_posts
        if order == 'New to Old':
            self.queryset = self.queryset[::-1]
        self.queryset = self.queryset[start:start + num_posts]
        serializer = PostSerializer(self.queryset, many=True)
        return Response([serializer.data, total, num_posts], status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        self.queryset = self.queryset.filter(username=pk)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatePostViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginGenericAPIView(generics.ListCreateAPIView):
    serializer_class = LoginSerializer
    queryset = Login.objects.all()
    permission_classes = []

    def list(self, request):
        self.queryset = self.queryset.filter(username=request.user.username)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AlertMessageViewSet(viewsets.ViewSet):
    serializer_class = AlertMessageSerializer
    permission_classes = []
    queryset = AlertMessage.objects.all()

    def list(self, request):
        return Response([], status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data['message'], status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        self.queryset = AlertMessage.objects.filter(uuid=pk)
        serializer = self.serializer_class(self.queryset, many=True)
        for alert_message in self.queryset:
            alert_message.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
