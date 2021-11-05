from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include('webapp.urls')),
    path('useraccount/',include('useraccount.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('api/v1/',include('apis.urls')),
    path('member/',include('membership.urls')),
]

if settings.DEBUG:
    # urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)