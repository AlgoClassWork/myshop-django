from django.contrib import admin

from store.models import Category, Order, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)