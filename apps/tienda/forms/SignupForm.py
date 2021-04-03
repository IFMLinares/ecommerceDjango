from django import forms
from django.contrib.auth import get_user_model

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone']

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Télefono'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder':'apellido'}),
            'phone': forms.TextInput(attrs={'placeholder':' +56949806952'})
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()