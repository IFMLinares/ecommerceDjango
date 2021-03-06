
import os
import random
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.utils import timezone
from xhtml2pdf import pisa
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from .forms.forms import CheckoutForm
from .models import Item, Order, User, OrderItem, Address, Comuna, PagosWebpay
# Create your views here.
# options de produccion
optionsWebpay = WebpayOptions('597037518328','2a8701f54511fbaaf4a82a9b5fa0e597',IntegrationType.LIVE)
# options de integracion
# optionsWebpay = WebpayOptions('597055555532','579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',IntegrationType.TEST)

# url Production
urlSite = 'https://www.llona.cl/'
# url integration
# urlSite = 'http://localhost:8000/'

"""
    Vistas del sitio web a usar:
        HomeView = Pantalla de inicio
        ItemsListView = Listado de los productos
        ItemDetailView = detalles de un producto único
        OrderSumaryView = Listado de productos en el carro
        UserProfileView = Vista y edición de los detalles del usuario
        CheckoutView = Vista para chequear la compra
        ContactView = Información para el contacto
        WebpayConfirm = Vista para confirmar el pago del webpay
"""

def WebpayConfirm(request):
    if request.POST['token_ws']:
        token = request.POST['token_ws']
        response = Transaction.commit(token, optionsWebpay)
        if response.response_code == 0 and response.status == 'AUTHORIZED':
            order = Order.objects.get(tokenWp=token, ordered=False)
            pago = PagosWebpay(
                webpay_token = token,
                monto = response.amount,
                fecha_transcaccion = response.transaction_date,
                orden_De_compra = response.buy_order,
                id_sesion = response.session_id,
                estado = response.status
            )
            pago.save()
            order.ordered = True
            order.pago = pago
            order.save()
            context = {
                'token': token,
                'response': response,
                'orden': order
            }
            usuario = User.objects.get(username=order.user.username)
            message = """
            EL USUARIO: %s A FINALIZADO CON EXITO UNA COMPRA DE $$%s \r\r\n
            DATOS DEL COMPRADOR:
            NOMBRE Y APELLIDO: %s %s \r\r\n
            TELEFONO: %s \r\r\n
            POR FAVOR VE AL ADMINISTRADOR PARA VERIFICAR LA COMPRA.
            """ % (usuario.username, order.totalOrden, usuario.first_name, usuario.last_name, usuario.phone)
            body = render_to_string(
                'email_content.html',{
                    'message': message
                },
            )
            email_message = EmailMessage(
                subject='COMPRA FINALIZADA',
                body = body,
                from_email= 'inversionesllonaspa@gmail.com',
                to = ['inversionesllonaspa@gmail.com']
            )
            email_message.content_subtype = 'html'
            email_message.send()

            return render(request, 'confirm.html', context)
        else:
            token = request.POST['token_ws']
            order = Order.objects.get(tokenWp=token, ordered=False)
            order.tokenWp.delete(save=False)
            order.save()
    else:
        tbk_token = request.POST['TBK_TOKEN']
        tbk_orden_compra = request.POST['TBK_ORDEN_COMPRA']
        tbk_id_sesion = request.POST['TBK_ID_SESION']
        context = {
            'tbk_token': tbk_token,
            'tbk_orden_compra': tbk_orden_compra,
            'tbk_id_sesion': tbk_id_sesion
        }
        return render(request, 'confirm.html', context)

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            user = User.objects.get(username=self.request.user.username)
            comunas = Comuna.objects.all().order_by('nombre')
            json_data = serialize("json",comunas)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'user': user,
                'json': json_data
            }
            return render(self.request, 'check-out.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'No tienes ninguna orden activa')
            return redirect('core:checkout')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if self.request.POST['select'] == 'retiro':
                mount = self.request.POST['mount']
                messages.success(self.request, "Puede Proceder al formulario de pago con retiro en tienda")

                buy_order = order.pk
                session_id = order.pk
                return_url = urlSite+'confirm/'

                response = Transaction.create(buy_order, session_id, mount, return_url, optionsWebpay)
                order.totalOrden = mount
                order.tipo_Retiro = 'tienda'
                order.tokenWp = response.token
                order.save()

                context = {
                    'response': response
                }

                return render(self.request, 'prueba.html', context)
            elif self.request.POST['select'] == 'starken':
                if form.is_valid():
                    street_address =form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    mensaje = form.cleaned_data.get('description')
                    retiro = 'starken'
                    comuna = self.request.POST['comunaStarken']
                    # same_shipping_address =form.cleaned_data.get('same_shipping_address')
                    # save_info =form.cleaned_data.get('save_info')
                    address = Address(
                        user = self.request.user,
                        street_address = street_address,
                        apartment_address = apartment_address,
                        comuna = comuna
                    )
                    address.save()
                    order.billing_address = address
                    order.message = mensaje
                    order.tipo_Retiro = retiro
                    mount = self.request.POST['mount']
                    order.totalOrden = mount
                    messages.success(self.request, "Puede Proceder al formulario de pago")
                    buy_order = random.randint(1,300)
                    session_id = random.randint(1,300)
                    amount = mount
                    return_url = urlSite + 'confirm/'
                    response = Transaction.create(buy_order, session_id, amount, return_url, optionsWebpay)
                    order.tokenWp = response.token
                    order.save()
                    context = {
                        'response': response
                    }
                    return render(self.request, 'prueba.html', context)
            elif self.request.POST['select'] == 'delivery':
                if form.is_valid():
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    mensaje = form.cleaned_data.get('description')
                    retiro = 'delivery'
                    comuna = self.request.POST['comuna']
                    # same_shipping_address =form.cleaned_data.get('same_shipping_address')
                    # save_info =form.cleaned_data.get('save_info')
                    address = Address(
                        user = self.request.user,
                        street_address = street_address,
                        apartment_address = apartment_address,
                        comuna = comuna
                    )
                    address.save()
                    order.billing_address = address
                    order.message = mensaje
                    order.tipo_Retiro = retiro
                    deliveryPrice = Comuna.objects.get(nombre=comuna)
                    precio = int(deliveryPrice.precio)
                    deliveryPrice = precio
                    mount = int(self.request.POST['mount']) + precio
                    order.totalOrden = mount
                    messages.success(self.request, "Puede Proceder al formulario de pago")
                    buy_order = random.randint(1,300)
                    session_id = random.randint(1,300)
                    amount = mount
                    return_url = urlSite + 'confirm/'
                    response = Transaction.create(buy_order, session_id, amount, return_url, optionsWebpay)
                    order.tokenWp = response.token
                    order.save()
                    context = {
                        'response': response
                    }
                    return render(self.request, 'prueba.html', context)
            else:
                return ('core:checkout')
            messages.warning(self.request, "Pago Fallido")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna orden activa')
            return redirect('/')

# vista del inicio
class HomeView(ListView, User):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self):
        items = list(self.model.objects.filter(ocultar=False).order_by('title'))
        if len(items) > 0 and len(items) >= 5 :
            items = random.sample(items,5)
            return items
        elif len(items) > 0 and len(items)<5:
            items = random.sample(items,len(items))
            return items
        else:
            items = 'No hay productos para mostrar'
            return items

# vista para el listado de productos
class ItemsListView(ListView):
    model = Item
    paginate_by = 9
    template_name = 'shop.html'
    context_object_name = 'items'

    def get_queryset(self):
        return self.model.objects.filter(ocultar=False).order_by('title')

# vista detallada de los productos
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item'

# vista del carrito de compras (detallado)
class OrderSumaryView(LoginRequiredMixin, View):
    model = Order
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            items = Item.objects.all().only('slug', 'tallas')
            cantidad = 0
            for item in order.items.all():
                cantidad += item.quantity
            if cantidad == 1:
                for item in order.items.all():
                    a = Item.objects.get(pk=item.item.pk)
                    precio = a.price
                    item.totalItem = precio
                    item.save()
            elif cantidad == 2:
                precio = 10495
                for item in order.items.filter(item__categoria__nombre='Poleras'):
                    item.totalItem = precio
                    item.save()
            else:
                precio = 9663.33333333332
                for item in order.items.filter(item__categoria__nombre='Poleras'):
                    item.totalItem = precio
                    item.save()
            context = {
                'carro': order,
                'items': items
            }
            return render(self.request, 'shopping-cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna orden activa')
            return redirect('/')

# Clase para editar el perfil de usuario
class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'userProfile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        ordenes = Order.objects.filter(ordered=True)
        context = {
            'user': user,
            'order': ordenes
        }
        return render(self.request, 'userProfile.html', context)

# Clase para la seccion de contacto
class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        body = render_to_string(
            'email_content.html',{
                'name': name,
                'email': email,
                'message': message
            },
        )

        email_message = EmailMessage(
            subject='Mensaje de usuario',
            body = body,
            from_email=email,
            to = ['inversionesllonaspa@gmail.com']
        )
        email_message.content_subtype = 'html'
        email_message.send()

        return redirect('core:contact')

class AboutView(TemplateView):
    template_name = 'about-us.html'

""" Funciones para el funcionamiento del carrito de compras
    Ejemplo:
        add_to_cart (añadir al carrito)
        remove_single_item_from_cart (remover un articulo del carro)
        remove_from_cart (remover todas las cantidades de un item del carro)
"""

# función de añadir al carro
@login_required
def addto(request):
    if request.method=='POST':
        slug = request.POST['slug']
        size = request.POST['size']
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(talla=size, item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # verificando si el item odernado ya está en la orden
            if order.items.filter(item__slug=item.slug, talla=size).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, 'La cantidad de este producto fue actualizada satisfactoriamente')
                return redirect('core:list-product')
            else:
                order.items.add(order_item)
                messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
                return redirect('core:list-product')
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, 'Este producto fue añadido satisfactoriamente a su carrito')
        return redirect('core:list-product')

@login_required
def add_to_cart(request, slug, talla):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(talla=talla, item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug, talla=talla).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'La cantidad de este producto fue actualizada satisfactoriamente')
            return redirect('core:order-sumary')

# funcion para actualizar la talla del carro
@login_required
def update_size(request):
    if request.method=='POST':
        oldSize = request.POST['oldsize']
        newsize = request.POST['talla']
        slug = request.POST['slug']
        return redirect('core:home')

# función para restar 1 del carrito
@login_required
def remove_single_item_from_cart(request, slug, talla):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug, talla=talla).exists():
            order_item = OrderItem.objects.filter(item=item, talla=talla, user=request.user, ordered=False)[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save() 
            else:
                return redirect('core:remove-from-cart', slug=slug, talla=talla)
        else:
            messages.info(request, 'Este producto no está en su carrito')
            return redirect('core:order-sumary')
    else:
        messages.info(request, 'Justo ahora no tienes ninguna orden activa')
        return redirect('core:order-sumary')

    return redirect('core:order-sumary')

# funcion para remover todo un item del carrito
@login_required
def remove_from_cart(request, slug, talla):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificando si el item odernado ya está en la orden
        if order.items.filter(item__slug=item.slug, talla=talla).exists():
            order_item = OrderItem.objects.filter(item=item, talla=talla, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Este Producto fue eliminado satisfactoriamente')
            return redirect('core:order-sumary')
        else:
            messages.info(request, 'Este producto no está en su carrito')
            return redirect('core:order-sumary', slug=slug)
    else:
        messages.info(request, 'Justo ahora no tienes ninguna orden activa')
        return redirect('core:order-sumary', slug=slug)

# FUNCION PARA CREAR PDFS
@login_required
def pdfFactura(request, pk):

    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
            # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    try:
        template = get_template('pdfFactura.html')
        order = Order.objects.filter(pk=pk)
        if order.exists():
            context = {
                'order': order,
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/1.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response, link_callback=link_callback)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            return HttpResponse('Consulta invalida')
    except:
        pass
    HttpResponseRedirect(reverse_lazy('core:home'))