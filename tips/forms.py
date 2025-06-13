from django import forms
from .models import Tip

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'How to avoid getting fat!!!'
            }),
            'description': forms.Textarea(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'You need to avoid fats',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'style': 'max-height: 100px; overflow-y: auto;',  # Scrollable dropdown
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',  # Hidden for styling
                'accept': 'image/*',
                'id': 'image-upload'
            })
        }
