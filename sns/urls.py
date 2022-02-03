from django.contrib import admin
from django.urls import path, include
from content.views import Main
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view()),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
