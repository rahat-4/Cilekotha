from distutils.archive_util import make_zipfile
from unicodedata import category
from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    main_image = models.ImageField(upload_to='product')
    name = models.CharField(max_length=264)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=300, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']