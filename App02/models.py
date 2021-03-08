from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=12, null=True, verbose_name='手机号')

    class Meta(AbstractUser.Meta):
        db_table = 'user'
