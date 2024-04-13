from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

#회원 모델
class User(models.Model):
    user_id = models.CharField(max_length=100, unique=True, primary_key=True)
    user_pw = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_gender = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user_id
        

#냉장고 모델
class Refrigerator(models.Model):
    refri_user_id = models.ForeignKey("User", related_name="refri_user", on_delete=models.CASCADE, db_column="refri_user_id")
    ingre_id = models.AutoField(primary_key=True)
    main_ingre = models.CharField(max_length=100)
    expiration = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.main_ingre
    
#레시피 모델
class Recipe(models.Model):
    recipe_id = models.BigAutoField(help_text="Recipe ID", primary_key=True)
    recipe_title = models.CharField(max_length=100)
    recipe_main_ingre = models.CharField(max_length=100)
    recipe_total_ingre = models.CharField(max_length=500)
    recipe_serving = models.CharField(max_length=100)
    recipe_time = models.CharField(max_length=100)
    recipe_order = models.CharField(max_length=1500, default='')
    recipe_image = models.CharField(max_length=200)
    
    def __str__(self):
        return self.recipe_title
    
#좋아하는 레시피 모델   
class Favorite_Recipe(models.Model):
    fav_id = models.AutoField(primary_key=True)
    fav_user_id = models.ForeignKey("User", related_name="fav_user", on_delete=models.CASCADE, db_column="fav_user_id")
    fav_recipe_id = models.ForeignKey("Recipe", related_name="fav_recipe", on_delete=models.CASCADE, db_column="fav_recipe_id")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    #복수 PK 만들기
    class Meta :
        constraints = [ 
            models.UniqueConstraint(
                fields=["fav_user_id","fav_recipe_id"],
                name="unique favorite",
            )
        ]

    def __str__(self):
        return '{} {}'.format(self.fav_recipe_id, self.rating)
    
# class Image(models.Model):
#     image_up = models.ImageField(null=True, upload_to='images/')
class Image(models.Model):
    image_up = models.ImageField(null=True,upload_to='images/')
        
    def __str__(self):
        return self.image_up.name
        