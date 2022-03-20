from django.db import models
import datetime
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.http import request

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, balance=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not name:
            raise ValueError('Users must have a valid name')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.name = name
        user_obj.balance = balance
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, name=None, password=None, balance=None):
        user = self.create_user(
            email, name=name, password=password, balance=balance,is_staff=True)
        return user

    def create_superuser(self, email, name=None, password=None, balance=None):
        user = self.create_user(email, name="newname", password=password, balance=1000,is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.email+' ' + str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Transactions(models.Model):
    From = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    Amount = models.IntegerField(null=True, blank=True)
    Currency = models.CharField(max_length=255, null=True, blank=True)
    To = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name="to")
    created_at = models.DateField(auto_now_add=True)
    Update_at = models.DateField(auto_now_add=True)
