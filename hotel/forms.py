from django import forms
from .models import Hotel, Menu,Cart

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name','location','phone','email']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title','description','menu_image','price','category','availability']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm',
                'placeholder': 'Enter the menu title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm',
                'placeholder': 'Enter the menu description',
            }),
            'menu_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm',
                'placeholder': 'Enter the price',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm',
            }),
            'availability': forms.CheckboxInput(attrs={
                'class': 'rounded',
            }),
        }

