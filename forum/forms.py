# forum/forms.py
from django import forms
from .models import Forum

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'desc']  # Use 'desc' instead of 'content'
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'id': 'comment-input',  # Assurez-vous que l'ID correspond à celui utilisé dans le JavaScript
            }),
        }

from .models import Response

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']  # Champ texte pour la réponse