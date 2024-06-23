from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = ""
    
    class Meta:
        model = Message
        fields = ('message',)

        widgets = {
            # 'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your name',}),
            # 'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter phone number',}),
            # 'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter phone email',}),
            'message' : forms.TextInput(attrs={'class':'form emailForm1 mx-auto d-flex flex-wrap pl-5 mr-5', 'placeholder':'...Enter your message...',}),
        }

