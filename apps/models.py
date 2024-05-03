import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    comment_count = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='blog/images/')
    category = models.ForeignKey('apps.Category', SET_NULL, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# ------------------------------------ email verification --------------------------------------------
class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    activation_link_used = models.BooleanField(default=False)


# -----------------JSONFIELD------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/%Y/%m', null=True)
    description = models.TextField(null=True, blank=True)
    info = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


'''
django i18n

LANGUAGES(
    ()
    ()

)

LOCALE_PATHS = [BASE_DIR / 'locale']

verbose_name = _('products')
gettext_lazy as _
i18n_patterns (urls.py)
'''
