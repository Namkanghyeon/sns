from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    '''
        profile image
        user nickname
        user name
        user email address
        user password -> 일단 디폴트
    '''

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=24)  # 길이 제한 있음
    nickname = models.CharField(max_length=24, unique=True)
    profile_image = models.TextField()  # 길이 제한 없음

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = 'User'
