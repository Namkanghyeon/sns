import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from sns.settings import MEDIA_ROOT


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
                            profile_image='default_profile.jpeg'
                            )

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message='회원정보가 잘못되었습니다.'))

        if user.check_password(password):
            # 세션에 로그인 정보 넣기
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message='회원정보가 잘못되었습니다.'))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        email = request.data.get('email')

        profile_image = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, profile_image)
        # media 디렉토리에 이미지 파일 자체를 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        user = User.objects.filter(email=email).first()
        user.profile_image = profile_image
        user.save()

        return Response(status=200)
