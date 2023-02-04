from django.contrib import admin
from .models import Client, ClientAddres, Product, Order, orderItems
# Register your models here.
admin.site.register(Client)
admin.site.register(ClientAddres)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(orderItems)
