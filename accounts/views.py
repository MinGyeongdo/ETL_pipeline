from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics

# 로그인은 Django REST Framework에서 제공되는 URL 이용

# 회원가입
# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer