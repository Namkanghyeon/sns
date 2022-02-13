from uuid import uuid4
import boto3

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from sns.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        email = request.data.get('email', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)
        password = request.data.get('password', None)
        profile_image = f'https://s3.ap-northeast-2.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/static/default_profile.jpeg'

        User.objects.create(email=email,
                            name=name,
                            nickname=nickname,
                            password=make_password(password),
                            profile_image=profile_image
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
            request.session['email'] = email  # 세션에 로그인 정보 넣기
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message='회원정보가 잘못되었습니다.'))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class ProfileImage(APIView):
    def post(self, request):
        file = request.FILES['file']
        email = request.data.get('email')

        image_name = uuid4().hex
        save_path = f'https://s3.ap-northeast-2.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/profile_image/{image_name}'

        # s3에 upload
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3_client.upload_fileobj(
            file,
            AWS_STORAGE_BUCKET_NAME,
            f'profile_image/{image_name}',
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # image url을 User table에 저장
        user = User.objects.filter(email=email).first()
        user.profile_image = save_path
        user.save()

        return Response(status=200)
