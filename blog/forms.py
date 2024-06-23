from django import forms
from .models import *

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('body','name', 'email',)
        
        widgets = {
            'body' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'comment', 'style': 'width: 200%;'}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your email...'}),
        }
        
        
class UserReplyCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('body','name',)
        
        widgets = {
            'body' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'comment', 'style': 'height: 70px'}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
        }
