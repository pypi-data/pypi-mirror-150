from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, SetNewPasswordSerializer
from .utils import Util

User = get_user_model()

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = []
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        return Response(
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            status=status.HTTP_200_OK
        )
    
    def update(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        user.username = request.data['username']
        user.email = request.data['email']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        if (request.data['password'] != 'update'):
            user.set_password(request.data['password'])
        user.save()
        return Response(
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

class ChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def update(self, request, pk=None):
        user = User.objects.get(username=pk)
        user.set_password(request.data['password'])
        user.save()
        return Response('Password reset', status=status.HTTP_200_OK)

class RequestPasswordResetGenericAPIView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = []

    def post(self, request):
        username = request.data['username']
        if len(User.objects.filter(username=username)) > 0:
            user = User.objects.get(username=username)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('reset-password', kwargs={ 'uidb64': uidb64, 'token': token })
            # absurl = 'http://' + current_site + relative_link
            absurl = 'http://localhost:3000/change_password?uidb64=' + uidb64 + '&token=' + token + '&username=' + username
            email_body = 'Reset password using the following link:\n\n' + absurl
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset Password'
            }
            Util.send_email(data)
            return Response({ 'success': 'A link has been sent to your email where you can reset your password.' }, status=status.HTTP_201_CREATED)
        return Response({ 'error': 'There is no user with username "' + request.data['username'] + '".' }, status=status.HTTP_404_NOT_FOUND)

class PasswordTokenCheckGenericAPIView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({ 'error': 'Token is not valid, please request a new one.' }, status=status.HTTP_400_BAD_REQUEST)
            return Response({ 'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token, 'username': user.username }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({ 'error': 'Token is not valid, please request a new one.' }, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordGenericAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({ 'success': True, 'message': 'Password reset successful.' }, status=status.HTTP_200_OK)
