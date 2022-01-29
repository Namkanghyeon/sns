from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password


class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        email = request.data.get('email', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            name=name,
                            nickname=nickname,
                            password=make_password(password),
                            profile_image='default_profile.jpg'
                            )

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        pass
