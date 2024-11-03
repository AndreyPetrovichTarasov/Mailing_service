from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('clients/', include('clients.urls', namespace='clients')),
    path('mailings/', include('mailings.urls', namespace='mailings')),
    path('messages_list/', include('messages_list.urls', namespace='messages_list')),
]

# Обработка медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
