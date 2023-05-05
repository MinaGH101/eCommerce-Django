from django import forms
from .models import Shipping

class SearchForm(forms.Form):
    search_bar = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'search product...'}))
    
    
class ShippingForm(forms.ModelForm):
    
    class Meta:
        model = Shipping
        fields = ('first_name', 'last_name','phone', 'address1', 'address2', 'area', 'state', 'postal_code')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your first name',}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your last name',}),
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter phone number',}),
            'address1' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'address2' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'area' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'state' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'postal_code' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
        }

        
class SizeForm(forms.Form):
    size_L = forms.BooleanField(label='L', required=False)
    size_M = forms.BooleanField(label='M', required=False ,initial=True)
    size_S = forms.BooleanField(label='S', required=False)
    
    
class NoteForm(forms.Form):
    note = forms.Textarea()
        