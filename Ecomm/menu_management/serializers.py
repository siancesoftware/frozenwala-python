

from rest_framework import serializers
from .models import Item
from ecomApp.models  import Catagory,Stock, DeliveryCharge

from ecomApp.models import Catagory

class ItemSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    item_photo = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_item_photo(self, obj):
        if obj.item_photo:
            # Extract just the filename
            filename = obj.item_photo.name.split('/')[-1]
            # Construct the new URL path
            return f"https://bill.megasgoods.com/uploads/items/{filename}"
        return "https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png"

    def get_stock(self, obj):
        # Assuming the related Stock model is linked via a ForeignKey or OneToOneField on Item
        # and the 'openingStock' is a field on the Stock model.
        stock = Stock.objects.filter(item_id=obj).first()  # Adjust based on the actual relationship
        return stock.openingstock if stock else None




class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Catagory
        fields = '__all__'
    def get_image(self, obj):
           if obj.image:
               # Extract just the filename
               filename = obj.image.name.split('/')[-1]
               # Construct the new URL path
               return f"https://bill.megasgoods.com/uploads/category/{filename}"
           return "https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png"
