from django.contrib import admin

# Register your models here.
from refrigerator.models import User, Refrigerator, Favorite_Recipe, Recipe, Image

#테이블 등록
admin.site.register(User)
admin.site.register(Refrigerator)
admin.site.register(Favorite_Recipe)
admin.site.register(Recipe)
admin.site.register(Image)