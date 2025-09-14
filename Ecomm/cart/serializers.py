from rest_framework import serializers
from .models import Cart


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['product_id'] = instance.product_id.id
#         representation['item_photo'] = instance.product_id.item_photo.url if instance.product_id.item_photo else None
#         representation['product_image'] = instance.product_id.item_photo.url if instance.product_id.item_photo else None
#         representation['item_new_price'] = "{:.2f}".format(instance.product_id.item_new_price)
#         representation['totalPrice'] = "{:.2f}".format(instance.price)
#         representation['title'] = instance.product_id.title
#         representation['product_name'] = instance.product_id.title
#         return representation
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Get the filename of the item photo
        item_photo = instance.product_id.item_photo
        photo_url = 'https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png'
        if item_photo:
            filename = item_photo.name.split('/')[-1]
            photo_url = f"https://bill.megasgoods.com/uploads/items/{filename}"

        # Custom fields
        representation['product_id'] = instance.product_id.id
        representation['item_photo'] = photo_url
        representation['product_image'] = photo_url
        representation['item_new_price'] = "{:.2f}".format(instance.product_id.item_new_price)
        representation['totalPrice'] = "{:.2f}".format(instance.price)
        representation['title'] = instance.product_id.title
        representation['product_name'] = instance.product_id.title

        return representation

class CartGetSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_id.title', read_only=True)
    product_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return "{:.2f}".format(obj.price)

    def get_product_image(self, obj):
        item_photo = obj.product_id.item_photo
        if item_photo:
            filename = item_photo.name.split('/')[-1]
            return f"https://bill.megasgoods.com/uploads/items/{filename}"
        return "https://admin.frozenwala.com/media/videos/Frozenwala_logo_English-1_fghT31B.png"
    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'u_id', 'quantity', 'price', 'product_name', 'product_image']
