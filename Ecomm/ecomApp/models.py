from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.shortcuts import reverse
from django.utils import timezone
from decimal import Decimal
import random
from django.contrib.auth.models import User
from django.conf import settings
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        user = self.model(phone_number=phone_number, name=name, referral_code=referral_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, name, referral_code, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id= models.AutoField(primary_key=True)
    otp_value = models.CharField(max_length=6, blank=True)
    is_influencer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True)  # You can adjust the max_length as needed.
    name = models.CharField(max_length=255,null=True)
    influencer_code = models.CharField(max_length=255,null=True)

    registration_id = models.CharField(max_length=255,null=True)
    # otp=models.CharField(max_length=6,null=True)
    bio=models.CharField(max_length=255,default='')
    profile_photo=models.ImageField(upload_to='videos/', null=True, blank=True)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    # password = models.CharField(max_length=128)  # Store the password as a hash.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_blocked_by')
    status = models.IntegerField(default=1)
    walet=models.FloatField(default=11)
    email = models.EmailField()
    # referral_link = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # slug = models.CharField(max_length=15, blank=True,unique=True, null=True)
    objects = CustomUserManager()
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.PositiveIntegerField(default=1)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    # def save(self, *args, **kwargs):
    #     if not self.walet:
    #         self.walet = 11.0
    #     super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.id}"


    #
    #
    #     super(CustomUser, self).save(*args, **kwargs)
    #     super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True  # Custom implementation if needed

    def has_module_perms(self, app_label):
        return True  # Custom implementation if needed

    class Meta:
        ordering = ['phone_number']  # Adjust ordering field

class Otp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    phone_number=models.CharField(max_length=20, blank=True)

class Catagory(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    status= models.BooleanField(default=True)
    flag= models.BooleanField(default=False)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    @property
    def clean_photo_url(self):
        """
        Custom image URL with /uploads/ prefix and category folder.
        Example: /uploads/snacks/filename.jpg
        """
        if self.image:
            filename = self.image.name.split('/')[-1]  # just the filename
            return f"https://bill.megasgoods.com/uploads/category/{filename}"
        return "https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png"
    def __str__(self):
        return self.name

    # def __getattribute__(self, name):
    #     # Intercept access to image.url
    #     if name == 'image' and object.__getattribute__(self, 'flag'):
    #         image = object.__getattribute__(self, 'image')
    #         if image:
    #             class ProxyFile:
    #                 def __init__(self, original):
    #                     self.original = original
    # 
    #                 @property
    #                 def url(self):
    #                     filename = self.original.name.split('/')[-1]
    #                     return f"https://bill.megasgoods.com/uploads/category/{filename}"
    # 
    #                 def __getattr__(self, attr):
    #                     return getattr(self.original, attr)
    # 
    #             return ProxyFile(image)
    # 
    #     return super().__getattribute__(name)


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)

    name= models.CharField(max_length=100)
    cat_name = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    price=models.IntegerField()
    coupon = models.IntegerField( blank=True, null=True)
    description=models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')
    status= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    barcode = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class CustomerCoupon(models.Model):
    id = models.AutoField(primary_key=True)
    coupon =  models.CharField(max_length=255)
    occasion = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    start_date = models.DateField()
    expire_date = models.DateField()
    coupon_value = models.CharField(max_length=255)
    coupon_type = models.CharField(max_length=20)
    description = models.TextField()
    status= models.BooleanField(default=True)
class DeliveryCharge(models.Model):
    id = models.AutoField(primary_key=True)
    charge =  models.IntegerField()
    status= models.BooleanField(default=True)
from menu_management.models import Item
class Stock(models.Model):
    id = models.BigAutoField(primary_key=True)
    openingstock=models.IntegerField(default=0)
    item_id=models.ForeignKey(Item,on_delete=models.CASCADE)
  #  pro_id= models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag= models.BooleanField(default=False)
    piece_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Stock for {self.item_id.title}: {self.openingstock}"
