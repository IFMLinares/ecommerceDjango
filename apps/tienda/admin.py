from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Item, OrderItem, Order, User, Size, Address, Comuna

# Register your models here.

# class ProductoResource(resources.ModelResource):
#     class Meta:
#         model = Item

# class TallaResource(resources.ModelResource):
#     class Meta:
#         model = Size

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User

# class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = ProductoResource

# class SizeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = TallaResource

# class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = UserResource
admin.site.register(Size)
admin.site.register(User)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Comuna)