from django import forms
from .models import Posts


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content','image']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 10})
        }
