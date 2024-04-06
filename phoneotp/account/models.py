from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username , email , phone_number , password=None , **extra_field):
        if username is None:
            return ValueError("User must have a username!")
        if email is None:
            return ValueError("User must have an E-mail address!")
        if phone_number is None:
            return ValueError("User must have an phone number!")
        
        user = self.model(username,email=self.normalize_email(email),phone_number=phone_number,**extra_field)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username , email , phone_number , password=None , **extra_field):
        extra_field.setdefault("is_superuser","True")
        extra_field.setdefault("is_staff","True")
        extra_field.setdefault("is_active","True")
        
        return self.create_user(username , email , phone_number ,password, **extra_field)
        

class User(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.IntegerField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, default=None, null=True, blank=True)
    
    
    objects = UserManager
    
    def __str__(self):
        return self.username + str(self.phone_number)