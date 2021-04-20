from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Item, OrderItem, Order, User, Size, Address, Comuna, PagosWebpay

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'tallas__talla',
        'ocultar',
        'price',
        'discount_price',
    )

class ComunasAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
    )

class DireccionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'comuna',
        'street_address',
        'apartment_address',
        'postal_code',
    )

class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tipoRetiro',
        'totalOrden',
        'ordered',
    )

class PagosAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'monto',
        'fecha_transcaccion',
    )

class ProductosOrdenadosAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quantity',
        'talla__talla',
        'ordered',
    )

admin.site.register(Size)
admin.site.register(User)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Comuna)
admin.site.register(PagosWebpay)