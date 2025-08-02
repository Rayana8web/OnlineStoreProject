from tabnanny import verbose

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choices import MyUserRoleEnum

# Create your models h
from django import forms
from django.contrib.auth import get_user_model

from django.conf import settings
#start
from django.utils import timezone
import random
import string

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser, PermissionsMixin ):
    username= models.CharField(max_length=222, verbose_name='Имя пользователя')
    email =  models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='media/user_avatars', null=True, blank=True, verbose_name='Аватар')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')

    role = models.CharField(
        max_length=20,
        choices=MyUserRoleEnum.choices,
        default = MyUserRoleEnum.STANDARD_USER,
        verbose_name = 'Роль'

    )
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Баланс')
    #start
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
#
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    #

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return (self.email)
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True



#start
    def generate_otp(self):
        code = ''.join(random.choices(string.digits, k=6))
        self.otp_code = code
        self.otp_created_at = timezone.now()
        self.save()
        return code

    def is_otp_valid(self, code):
        if not self.otp_code or self.otp_code != code:
            return False
        if timezone.now() - self.otp_created_at > timezone.timedelta(minutes=5):
            return False
        return True

