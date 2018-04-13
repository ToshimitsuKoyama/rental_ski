from django.contrib import admin
from .models import RentalMenuMaster,RentalMenuKindMaster,UserInfo,CustomerInfo

admin.site.register(RentalMenuMaster)
admin.site.register(RentalMenuKindMaster)
admin.site.register(UserInfo)
admin.site.register(CustomerInfo)
# Register your models here.
