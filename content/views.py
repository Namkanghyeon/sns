from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from sns.settings import MEDIA_ROOT
import os
from uuid import uuid4


class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')  # select * from content_feed
        return render(request, 'sns/main.html', context=dict(feed_list=feed_list))


class UploadFeed(APIView):
    def post(self, request):
        # 일단 파일을 불러옴
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image)

        return Response(status=200)
