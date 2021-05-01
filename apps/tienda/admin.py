from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Item, OrderItem, Order, User, Size, Address, Comuna, PagosWebpay, Category

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name', 'phone', 'rut']
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'rut',
    )

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'discount_price',
        'ocultar',
    )
    list_filter = ('ocultar', 'departamento', 'tallas', 'categoria')

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
    )
    readonly_fields = (
        'user',
        'comuna',
        'street_address',
        'apartment_address',
    )

class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tipo_Retiro',
        'totalOrden',
        'ordered',
    )
    list_filter = ('ordered', 'tipo_Retiro')
    readonly_fields = (
        'user',
        'ordered',
        'items',
        'tipo_Retiro',
        'ordered_date',
        'start_date',
        'message',
        'billing_address',
        'tokenWp',
        'totalOrden',
        'pago',
    )

# class PagosAdmin(admin.ModelAdmin):
#     list_display = (
#         'monto',
#         'fecha_transcaccion',
#     )

# class ProductosOrdenadosAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'quantity',
#         'ordered',
#     )


admin.site.register(Size)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(OrderItem, ProductosOrdenadosAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(Address, DireccionAdmin)
admin.site.register(Comuna, ComunasAdmin)
# admin.site.register(PagosWebpay, PagosAdmin)