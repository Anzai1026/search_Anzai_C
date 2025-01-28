from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('search_app.urls')),
    path('admin/', admin.site.urls),
]
