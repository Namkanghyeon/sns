from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Comment, Like, Bookmark
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
            comment_object_list = Comment.objects.filter(feed_id=feed.id)
            comment_list = []
            for comment in comment_object_list:
                comment_user = User.objects.filter(email=comment.email).first()
                comment_list.append(dict(
                    content=comment.content,
                    nickname=comment_user.nickname,
                ))
            feed_list.append(dict(
                id=feed.id,
                image=feed.image,
                content=feed.content,
                profile_image=user.profile_image,
                # like_count=feed.like_count,
                nickname=user.nickname,
                comment_list=comment_list,
            ))
        return render(request, 'sns/main.html', context=dict(feed_list=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        email = request.session.get('email', None)
        file = request.FILES['file']
        image = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, image)
        # media 디렉토리에 이미지 파일 자체를 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')

        Feed.objects.create(email=email, image=image, content=content)

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


class UploadComment(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        content = request.data.get('content', None)
        email = request.session.get('email', None)

        Comment.objects.create(feed_id=feed_id, content=content, email=email)

        return Response(status=200)
