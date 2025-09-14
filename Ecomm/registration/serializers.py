# serializers.py
from rest_framework import serializers
from ecomApp.models import CustomUser
# class RegistrationSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     otp = serializers.CharField()
class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number',  'otp_value','name','influencer_code')

    def create(self, validated_data):
        # Set the walet attribute to 0.0 in the validated_data dictionary
        # validated_data['walet'] = 11.0

        # Create the user with the updated validated_data
        user = CustomUser.objects.create_user(**validated_data)
        return user



class ProfileSerializer(serializers.ModelSerializer):
    referral_link = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': False},
            'phone_number': {'required': False},
            'email': {'required': False},
        }

    def get_referral_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/ref/frzn/?referral_code={obj.referral_code}')
        return None
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'bio','profile_photo']
        extra_kwargs = {
            'password': {'required': False},  # Allow password to be optional
            'email': {'required': False},  # Make email optional
            'bio': {'required': False},
            'name': {'required': False},
            # Make bio optional
            'profile_photo': {'required': False},
        }

from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
# address/serializers.py
from rest_framework import serializers
from .models import AddressAdmin

class AddressAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressAdmin
        fields = '__all__'
