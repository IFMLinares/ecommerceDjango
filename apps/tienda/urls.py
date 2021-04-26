from django.urls import path, include
from django.views.generic import TemplateView
from apps.tienda.views import (
    HomeView,
    ItemsListView,
    ItemDetailView,
    UserProfileView,
    OrderSumaryView,
    CheckoutView,
    ContactView,
    AboutView,
    add_to_cart,
    addto,
    update_size,
    remove_single_item_from_cart,
    remove_from_cart,
    WebpayConfirm,
    pdfFactura
)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-list/', ItemsListView.as_view(), name='list-product'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('user/<pk>', UserProfileView.as_view(), name='user'),
    path('cart/', OrderSumaryView.as_view(), name='order-sumary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about-us'),
    path('add-to-cart/<slug>/<talla>/', add_to_cart, name='add-to-cart'),
    path('addto/', addto, name='addto'),
    path('update-size/', addto, name='update-size'),
    path('confirm/', WebpayConfirm, name='confirm'),
    path('pdf-fact/<pk>/', pdfFactura, name='fact'),
    path('remove-from-cart/<slug>/<talla>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-from-cart/<slug>/<talla>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),

]

# URLS DE VISTAS IMPLICITAS
urlpatterns += [
    path('index-product-list/', TemplateView.as_view(
                                    template_name='shop.html'
                                    ), 
                                    name='index-list-product'),
]