from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from user.models import User
from sns.settings import MEDIA_ROOT
import os
from uuid import uuid4


class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        feed_object_list = Feed.objects.all().order_by('-id')  # select * from content_feed
        feed_list = []
        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            feed_list.append(dict(image=feed.image,
                                  content=feed.content,
                                  profile_image=user.profile_image,
                                  like_count=feed.like_count,
                                  nickname=user.nickname))
        return render(request, 'sns/main.html', context=dict(feed_list=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        image = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, image)
        # media 디렉토리에 이미지 파일 자체를 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image=image, content=content, email=email, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')
        return render(request, 'content/profile.html', context=dict(user=user))
