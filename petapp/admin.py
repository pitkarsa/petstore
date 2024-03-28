from django.contrib import admin
from petapp.models import Pet,Cart, Order

# Register your models here.

class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','breed','gender','age','price','details','pimage']
    list_filter = ['type','breed','price']

admin.site.register(Pet, PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','uid','pid','quantity']
    list_filter = ['uid']

admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','orderid','uid','pid','quantity']

admin.site.register(Order,OrderAdmin)