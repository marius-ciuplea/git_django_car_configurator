from django.db import models
from django.contrib.auth.models import User

class CarModel(models.Model):
    company_name = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=20000.000, null=True, blank=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.model_name}"



class Engine(models.Model):
    car_model = models.ForeignKey(CarModel, related_name='engines', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    types = models.CharField(max_length=100)
    power = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,  null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.power} HP" 

class Color(models.Model):
    car_model = models.ForeignKey(CarModel, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,  null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class ColorImage(models.Model):
    color = models.ForeignKey(Color, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image for {self.color}"

class Wheel(models.Model):
    car_model = models.ForeignKey(CarModel, related_name='wheels', on_delete=models.CASCADE)  # Now linked to a car model
    size = models.IntegerField()
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,  null=True, blank=True)
    
    def __str__(self):
        return f"{self.size}\" - {self.style}"

class Configuration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    engine = models.ForeignKey(Engine, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    wheel = models.ForeignKey(Wheel, on_delete=models.SET_NULL, null=True)
    offered_config = models.BooleanField(default=False, blank=True, null=True)
    offered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def total_price(self):
        
        return (
            self.car_model.base_price +
            (self.engine.price if self.engine else 0) +
            (self.color.price if self.color else 0) +
            (self.wheel.price if self.wheel else 0)
        )
        

        
    def __str__(self):
        return f"{self.user.username}'s {self.car_model.model_name} config"
    