from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views  # サインアップビューはここで定義

urlpatterns = [
    path('', views.search_view),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),  # サインアップ用ビュー
    path('search/', views.search_view, name='search_view'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/',  views.product_update, name='product_update'),
    path('product/<int:pk>/delete',  views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
