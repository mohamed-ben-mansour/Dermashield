from django import forms
from .models import Tip

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'description','category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'How to avoid getting fat !!!'
            }),
            'description': forms.Textarea(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'You need to avoid fats',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'style': 'max-height: 100px; overflow-y: auto;'  # Make the dropdown scrollable
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',  # Keep input hidden for enhanced styling
                'accept': 'image/*',
                'id': 'image-upload'
            })
        }

    # Custom label for image upload area with drag-and-drop style
    image_label = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'image-upload-label border-4 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center h-60 p-4 cursor-pointer hover:border-blue-400 transition ease-in duration-200 text-center',
            'style': 'background-image: url("https://img.freepik.com/free-vector/image-upload-concept-landing-page_52683-27130.jpg?size=338&ext=jpg"); background-size: contain; background-position: center;',
            'placeholder': 'Drag & Drop or Click to Upload',
            'onclick': "document.getElementById('image-upload').click()"
        })
    )