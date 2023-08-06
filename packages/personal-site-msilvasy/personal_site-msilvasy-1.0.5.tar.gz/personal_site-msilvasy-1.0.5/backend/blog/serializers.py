from .models import Post, Login, AlertMessage
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    post = serializers.CharField()
    date = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Post
        fields = ('title', 'post', 'date', 'name', 'username')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class AlertMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertMessage
        fields = '__all__'
