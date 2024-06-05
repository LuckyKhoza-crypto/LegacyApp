from .models import *
from django import forms


class CommentForm(forms.ModelForm):

    author = forms.CharField(max_length=100)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']
