from django import forms 

PAYMENT_OPTIONS = (
    ('W','WebPay'),
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'', 'class':'street-first'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'', 'class':'street-first'
    }))
    postal_code = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'dejenos un mensaje aquí', 'class':'street-first form-control', 'style':'resize: both;', 'cols':'40', 'rows':'5'
    }))

    