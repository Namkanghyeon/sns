import boto3
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Comment, Like, Bookmark
from user.models import User
from sns.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
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
            feed_user = User.objects.filter(email=feed.email).first()
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            comment_object_list = Comment.objects.filter(feed_id=feed.id)
            comment_list = []
            for comment in comment_object_list:
                comment_user = User.objects.filter(email=comment.email).first()
                comment_list.append(dict(
                    content=comment.content,
                    nickname=comment_user.nickname,
                ))
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(
                id=feed.id,
                image=feed.image,
                content=feed.content,
                profile_image=feed_user.profile_image,
                like_count=like_count,
                nickname=feed_user.nickname,
                comment_list=comment_list,
                is_liked=is_liked,  # 내가 이 피드에 좋아요를 눌렀는지
                is_marked=is_marked,  # 내가 이 피드에 북마크를 눌렀는지
            ))
        return render(request, 'sns/main.html', context=dict(feed_list=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        email = request.session.get('email', None)
        file = request.FILES['file']
        content = request.data.get('content')

        image_name = uuid4().hex
        save_path = f'https://s3.ap-northeast-2.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/feed_image/{image_name}'

        # s3에 upload
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3_client.upload_fileobj(
            file,
            AWS_STORAGE_BUCKET_NAME,
            f'feed_image/{image_name}',
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # image url을 feed table에 저장
        Feed.objects.create(email=email, image=save_path, content=content)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')
        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        my_feed_list = Feed.objects.filter(email=email).all()
        my_like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        my_like_feed_list = Feed.objects.filter(id__in=my_like_list)
        my_bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        my_bookmark_feed_list = Feed.objects.filter(id__in=my_bookmark_list)

        return render(request, 'content/profile.html', context=dict(
            user=user,
            my_feed_list=my_feed_list,
            my_like_feed_list=my_like_feed_list,
            my_bookmark_feed_list=my_bookmark_feed_list
        ))


class UploadComment(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        content = request.data.get('content', None)
        email = request.session.get('email', None)

        Comment.objects.create(feed_id=feed_id, content=content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        is_like = request.data.get('is_like', True)
        if is_like == 'true':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like_object = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like_object:
            like_object.is_like = is_like
            like_object.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        is_marked = request.data.get('is_marked', True)
        if is_marked == 'true':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark_object = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark_object:
            bookmark_object.is_marked = is_marked
            bookmark_object.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)
