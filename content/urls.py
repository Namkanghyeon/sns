from django.urls import path
from .views import UploadFeed, Profile, UploadComment, ToggleLike, ToggleBookmark

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('profile', Profile.as_view()),
    path('comment', UploadComment.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
]
