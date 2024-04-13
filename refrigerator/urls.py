from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='refrigerator'

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('main_page/', views.main_page, name="main_page"),
    path('user_modify/', views.user_modify, name="user_modify"),
    path('user_delete/', views.user_delete, name="user_delete"),
    path('logout/', views.logout, name="logout"),
    path('total_recipe/', views.total_recipe, name='total_recipe'),
    path('detail_recipe/<ppk>', views.detail_recipe, name='detail_recipe'),
    path('total_recipe/<str:main_ing>', views.photo_recipe, name='photo_recipe'),
    path('fav_recipe/',views.fav_recipe, name="fav_recipe"),
    path('my_favorite/', views.my_recipe, name="my_recipe"),
    path('my_rec/', views.my_recommend_recipe, name="recommend_recipe"),
    path('image_upload/', views.image_upload, name="image_upload"),
    path('fridge_save/', views.fridge_save, name='my_fridge'),
] + static(settings.STATIC_URL, document_root=settings.REFRIGERAOR_STATIC_DIR) 