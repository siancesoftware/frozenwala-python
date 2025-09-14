from django.contrib import admin
from .models import Influencer,InfluencerOtp,InfluencerAmount,InfluencerLink, WithdrawRequest
admin.site.register(Influencer)
admin.site.register(InfluencerAmount)
admin.site.register(InfluencerOtp)
admin.site.register(InfluencerLink)
admin.site.register(WithdrawRequest)

# Register your models here.
