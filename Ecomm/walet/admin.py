from django.contrib import admin
from .models import Walet
from .models import PurchaseBenefit,ReferralBenefit,InstallationBenefit
admin.site.register(PurchaseBenefit)
admin.site.register(Walet)
admin.site.register(ReferralBenefit)
admin.site.register(InstallationBenefit)
