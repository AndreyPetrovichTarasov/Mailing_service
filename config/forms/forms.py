from django import forms
from clients.models import Client


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    message = forms.CharField(widget=forms.Textarea, label='Ваше сообщение')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']  # Укажите поля, которые вы хотите включить в форму
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
        }