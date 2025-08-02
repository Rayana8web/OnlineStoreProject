from django.db import models
from .constants import NULLABLE
#start
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
User = get_user_model()
from user.models import MyUser

class Category(models.Model):
    title = models.CharField(max_length=223, verbose_name='Название')
    cover = models.ImageField(upload_to='media/category_covers/')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='Родительская категория' )

    class Meta:
        verbose_name='Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        ancestors = []
        category = self
        while category:
            ancestors.append(category.title)
            category = category.parent_category
        return ' > '.join(reversed(ancestors))


class City(models.Model):
    title = models.CharField(max_length=223, verbose_name='Название')


    def __str__ (self):
        return self.title


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    title = models.CharField(max_length=223, verbose_name='Название')

    def __str__ (self):
        return self.title

class Image(models.Model):
    product=models.ForeignKey('Estate', on_delete=models.CASCADE)

    image=models.ImageField(upload_to='media/additional_image')

class Estate (models.Model):
    title = models.CharField(max_length=223, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    cover = models.ImageField(upload_to='media/products_image', verbose_name='Обложка')
    area = models.DecimalField( decimal_places=1, max_digits=12, verbose_name='Количество кв метров')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='Район')
    geo = models.TextField(verbose_name='Геолакация')
    price = models.DecimalField( decimal_places=2, max_digits=12, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    promo_vidio=models.FileField(upload_to='media/product_promo_vidio', verbose_name='Видео')
    is_active=models.BooleanField(default=True)
    # start
    liked_by = models.ManyToManyField(User, related_name='liked_ads', blank=True)


    class Meta:
        verbose_name='Недвижимость'
        verbose_name_plural = 'Недвижимость'

    #start
    def total_likes(self):
        return self.liked_by.count()
    #...
#

class Comment(models.Model):
    estate = models.ForeignKey('Estate', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} – {self.content[:20]}"

class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='favorites')


