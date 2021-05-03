from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Item, OrderItem, Order, User, Size, Address, Comuna, PagosWebpay, Category

# Register your models here.

class UserRsource(resources.ModelResource):
    class Meta:
        model = User

class ItemRsource(resources.ModelResource):
    class Meta:
        model = Item

class SizeRsource(resources.ModelResource):
    class Meta:
        model = Size

class ComunaRsource(resources.ModelResource):
    class Meta:
        model = Comuna

class CategoryRsource(resources.ModelResource):
    class Meta:
        model = Category

class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name', 'phone', 'rut']
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'rut',
    )
    list_per_page = 10

    resource_class = UserRsource

class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'discount_price',
        'ocultar',
    )
    list_filter = ('ocultar', 'departamento', 'tallas', 'categoria')
    search_fields = ['title']
    list_editable = ['ocultar']

    list_per_page = 10
    resource_class = ItemRsource

class ComunasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
    )
    resource_class = ComunaRsource

class SizeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SizeRsource

class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CategoryRsource

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

    list_per_page = 10

class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'get_status',
        'get_user',
        'get_nombre',
        'tipo_Retiro',
        'totalOrden',
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
        # 'tokenWp',
        'totalOrden',
        'pago',
    )
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'Usuario'
    get_user.admin_order_field = 'user__username'

    def get_nombre(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    get_nombre.short_description = 'Nombre y Apellido'

    def get_status(self, obj):
        if obj.ordered == True:
            return format_html(
                '<span style="color:green">PAGADO</span>&nbsp;',
            )
        else:
            return format_html(
                '<span style="color:red">NO PAGADO</span>&nbsp;',
            )
    get_status.short_description = 'ESTADO DE ORDEN'
    list_per_page = 10

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


admin.site.register(Size, SizeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(OrderItem, ProductosOrdenadosAdmin)
admin.site.register(Order, OrdenAdmin)
admin.site.register(Address, DireccionAdmin)
admin.site.register(Comuna, ComunasAdmin)
# admin.site.register(PagosWebpay, PagosAdmin)