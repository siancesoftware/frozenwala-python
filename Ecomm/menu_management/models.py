from django.db import models
from ecomApp.models import Catagory


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=500)
    description=models.CharField(max_length=1000)
    item_photo = models.ImageField(upload_to='item_photos/')
    # item_quantity = models.PositiveIntegerField()
    # item_measurement=models.CharField(max_length=10, default='')
    non_veg = models.BooleanField(default=False)
    item_old_price = models.FloatField()
    makingprice = models.FloatField()
    discount = models.IntegerField()
    piece_count = models.IntegerField(default=0)
    item_new_price = models.FloatField()
    status= models.BooleanField(default=True)
    veg=models.CharField(max_length=10,default='1')
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deal_of_the_day = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    most_popular = models.BooleanField(default=False)
    opening_stock = models.IntegerField(default=0)
    custom_barcode = models.CharField(max_length=10,default='0')

    def __str__(self):
        return f"Item ID: {self.id}, Category: {self.category.name}"

    @property
    def item_photo_url(self):
        """Returns the custom URL to the item photo without /media/."""
        if self.item_photo:
            filename = self.item_photo.name.split('/')[-1]
            return f"https://bill.megasgoods.com/uploads/items/{filename}"
        return "https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png"

    def __str__(self):
        return f"Item ID: {self.id}, Category: {self.category.name}"
    # def __getattribute__(self, name):
    #     # Intercept access to item_photo.url
    #     if name == 'item_photo' and object.__getattribute__(self, 'flag'):
    #         item_photo = object.__getattribute__(self, 'item_photo')
    #         if item_photo:
    #             class ProxyFile:
    #                 def __init__(self, original):
    #                     self.original = original
    #
    #                 @property
    #                 def url(self):
    #                     filename = self.original.name.split('/')[-1]
    #                     return f"https://bill.megasgoods.com/uploads/items/{filename}"
    #
    #                 def __getattr__(self, attr):
    #                     return getattr(self.original, attr)
    #
    #             return ProxyFile(item_photo)
    #
    #     return super().__getattribute__(name)