from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Item, OrderItem, Order, User, Size, Address, Comuna, PagosWebpay

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    search_fields = ['user__email']


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        # 'tallas__talla',
        'price',
        'discount_price',
        'ocultar',
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
    list_filter = ('ordered', 'tipoRetiro')

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
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, ProductosOrdenadosAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(Address, DireccionAdmin)
admin.site.register(Comuna, ComunasAdmin)
admin.site.register(PagosWebpay, PagosAdmin)