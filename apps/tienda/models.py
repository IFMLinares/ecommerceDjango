from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
import random

# Create your models here.

DEPARTAMENT_CHOICES = (
        ('C', 'Caballero'),
        ('D', 'Dama'),
    )

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class User(AbstractUser):
    phone = models.CharField(max_length=12)
    imagen = models.ImageField(upload_to = 'media/users', blank=True, null=True)
    rut = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username+ '\n ' + 'Nombre y Apellido: ' + self.first_name + ' ' + self.last_name

class Comuna(models.Model):
    nombre = models.CharField(max_length=20)
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = "Tienda: Comuna"
        verbose_name_plural = "Tienda: Comunas"

class Size(models.Model):
    talla = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to = 'media/users', blank=True, null=True)

    def __str__(self):
        return self.talla

    def save(self, *args, **kwargs):
        self.talla = self.talla.upper()
        super(Size, self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Tienda: Talla"
        verbose_name_plural = "Tienda: Tallas"

class Category(models.Model):
    nombre = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        verbose_name = "Tienda: Categoría"
        verbose_name_plural = "Tienda: Categorías"

    def __str__(self):
        return self.nombre

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    departamento = models.CharField(max_length=2, choices=DEPARTAMENT_CHOICES)
    tallas = models.ManyToManyField(Size)
    imagen = models.ImageField(upload_to = 'media')
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    ocultar = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        titulo = self.title
        depart = self.departamento
        num = random.randint(1, 1000)
        titulo = titulo.strip()
        self.slug = slugify('product-{}-{}-{}'.format(titulo, depart, num))
        super(Item, self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('core:product', kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={
            'slug': self.slug
        })
    def get_sizes(self):
        sizes = str([size for size in self.tallas.all().values_list('talla', flat=True)]).replace("[","").replace("]","").replace("'","").replace(",","")
        return sizes
    class Meta:
        verbose_name = "Tienda: Producto"
        verbose_name_plural = "Tienda: Productos"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    talla = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    totalItem = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.title} x{self.quantity} talla: {self.talla} \n"

    def get_total_item_price(self):
        return self.quantity * self.totalItem
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

    def espaciado(self):
        return 149 - (len(self.item.title) + 1)

    class Meta:
        verbose_name = "Producto Ordenado"
        verbose_name_plural = "Productos Ordenados"

class PagosWebpay(models.Model):
    webpay_token = models.TextField()
    monto = models.IntegerField(blank=True, null=True)
    orden_De_compra = models.CharField(max_length=240,blank=True, null=True)
    id_sesion = models.CharField(max_length=240,blank=True, null=True)
    estado = models.CharField(max_length=240,blank=True, null=True)
    fecha_transcaccion = models.CharField(max_length=240,blank=True, null=True)

    def __str__(self):
        return f"Estatus: {self.estado} \n Fecha de transaccion: {self.fecha_transcaccion} \n Orden de Compra: {self.orden_De_compra} \n Id de Sesión: {self.id_sesion}"

    class Meta:
        verbose_name = "Pago WebpayPlus"
        verbose_name_plural = "Pagos WebpayPlus"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    tipo_Retiro = models.CharField(max_length=9, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add= True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    billing_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    tokenWp = models.CharField(max_length=100, null=True, blank=True)
    totalOrden = models.IntegerField(blank=True, null=True)
    pago = models.OneToOneField(PagosWebpay, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__ (self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    class Meta:
        verbose_name = "Tienda: Orden"
        verbose_name_plural = "Tienda: Ordenes"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    comuna = models.CharField(max_length=20, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)

    def __str__(self):
        return f"Comuna: {self.comuna} \n Dirección Exacta: {self.street_address} \n Departamento {self.apartment_address}"

    class Meta:
        verbose_name = "Usuario: Dirección"
        verbose_name_plural = 'Usuario: Direcciones'
