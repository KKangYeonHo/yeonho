from django.contrib import admin
from django.urls import path, include
from refrigerator import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refrigerator/', include('refrigerator.urls'), name="refrigerator"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
