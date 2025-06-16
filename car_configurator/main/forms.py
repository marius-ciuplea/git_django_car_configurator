from django import forms
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
            self.fields['base_price'].initial = car_model.base_price
            self.fields['engine'].queryset = Engine.objects.filter(car_model=car_model)
            self.fields['color'].queryset = Color.objects.filter(car_model=car_model)
            self.fields['wheel'].queryset = Wheel.objects.filter(car_model=car_model)