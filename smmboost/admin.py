from django.contrib import admin
from .models import Wallet, Service, Order, WalletTransaction

# Register your models here.
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(WalletTransaction)
# from django.contrib.auth import get_user_model
