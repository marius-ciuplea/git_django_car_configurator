from django import forms
from django.contrib.auth.models import User
from .models import Profile, ContactForm

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Full Name'

  



class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        
        
class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message'}),
        }