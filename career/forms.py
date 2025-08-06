from django import forms
from .models import CareerApplication

class CareerApplicationForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['name', 'email', 'phone', 'cover_letter', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 shadow-sm focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-150',
                'placeholder': 'Your Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 shadow-sm focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-150',
                'placeholder': 'Your Email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 shadow-sm focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-150',
                'placeholder': 'Your Phone',
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 shadow-sm focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-150',
                'placeholder': 'Cover Letter',
                'rows': 5,
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'block w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-gray-900 placeholder-gray-400 shadow-sm focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-150',
            }),
        }
