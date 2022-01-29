from django.contrib import admin
from django.urls import path
from content.views import Main, UploadFeed
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Main.as_view()),
    path('content/upload', UploadFeed.as_view()),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
