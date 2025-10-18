from django import forms
from .models import InteriorInquiry

class InteriorInquiryForm(forms.ModelForm):
    class Meta:
        model = InteriorInquiry
        fields = ['name', 'email', 'phone', 'service_type', 'project_details', 'budget_range', 'timeline', 'location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Your Phone'
            }),
            'service_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-white/50',
                'style': 'color-scheme: dark;'
            }),
            'project_details': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50 resize-none',
                'placeholder': 'Tell us about your project',
                'rows': 4
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Budget Range (Optional)'
            }),
            'timeline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Expected Timeline (Optional)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50',
                'placeholder': 'Project Location (Optional)'
            }),
        }
