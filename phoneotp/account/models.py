from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.models import Permission as AuthPermission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if username is None:
            raise ValueError("User must have a username!")
        if email is None:
            raise ValueError("User must have an E-mail address!")
        if phone_number is None:
            raise ValueError("User must have a phone number!")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(username, email, phone_number, password=password, **extra_fields)

class User(AbstractUser):
  email = models.EmailField(max_length=50, unique=True)
  phone_number = models.IntegerField(unique=True)
  is_verified = models.BooleanField(default=False)
  otp = models.CharField(max_length=6, default=None, null=True, blank=True)

  objects = UserManager()

  user_permissions = models.ManyToManyField(AuthPermission, related_name='account_user_permissions')
  groups = models.ManyToManyField(AuthGroup, related_name='account_user_groups')

  def __str__(self):
    return self.username + str(self.phone_number)


