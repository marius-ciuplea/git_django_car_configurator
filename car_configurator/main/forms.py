from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CarModel, Configuration, Engine, Color, Wheel

class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['company_name', 'model_name']

class ConfigurationForm(forms.ModelForm):
    
    base_price = forms.DecimalField(
        disabled=True,
        label='Base Price',
        required=False
    )
    
    class Meta:
        model = Configuration
        fields = ['engine', 'color', 'wheel']

    def __init__(self, *args, **kwargs):
        car_model = kwargs.pop('car_model', None)
        super().__init__(*args, **kwargs)

        if car_model:
            # Filter the options based on the selected car model
            self.fields['base_price'].initial = car_model.base_price
            self.fields['engine'].queryset = Engine.objects.filter(car_model=car_model)
            self.fields['color'].queryset = Color.objects.filter(car_model=car_model)
            self.fields['wheel'].queryset = Wheel.objects.filter(car_model=car_model)
            
        
            # Customize the widget to display the engine, color, and wheel name as text
            self.fields['engine'].widget = forms.Select(choices=[(engine.id, engine.name) for engine in self.fields['engine'].queryset])
            self.fields['color'].widget = forms.RadioSelect(choices=[(color.id, color.name) for color in self.fields['color'].queryset])
            self.fields['wheel'].widget = forms.Select(choices=[(wheel.id, f"{wheel.size}\" - {wheel.style}") for wheel in self.fields['wheel'].queryset])


# User authentication, register
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_photo')  # you can add/remove fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
        
