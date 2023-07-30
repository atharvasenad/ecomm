from django.contrib import admin
from ecommapp.models import Products
# Register your models here.
# admin.site.register(Products)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','pdetails','is_active']
    list_filter=['cat','is_active']
admin.site.register(Products,ProductAdmin)