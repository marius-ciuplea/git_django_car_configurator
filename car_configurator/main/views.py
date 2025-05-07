from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import CarModel, Engine, Color, Wheel
from .forms import ConfigurationForm, CustomUserCreationForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = CarModel.objects.all()[:3]
        context['user'] = self.request.user 
        return context
    

class ConfigureView(TemplateView):
    template_name = 'configure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = CarModel.objects.all()
        return context

# Configure view

class ConfigureListView(TemplateView):
    template_name = 'configure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = CarModel.objects.all()
        return context

# Configure cars 
class ConfigureCarModelView(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        form = ConfigurationForm(car_model=car)  # Pass the car model to the form
        colors = Color.objects.filter(car_model=car)
        engines = Engine.objects.filter(car_model=car)
        wheels = Wheel.objects.filter(car_model=car)

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': colors,
            'engines': engines,
            'wheels': wheels
        })

    def post(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        form = ConfigurationForm(request.POST, car_model=car)  # Pass the car model to filter options

        if form.is_valid():
            configuration = form.save(commit=False)
            configuration.car_model = car
            configuration.save()
            return redirect('home')  # Redirect after saving the configuration

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form
        })




# # login view

# class CustomLoginView(LoginView):
#     template_name = 'login.html'

#     def form_invalid(self, form):
#         messages.error(self.request, 'Invalid credentials')
#         return super().form_invalid(form)


class LoginView(View):
    template_name = 'auth.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'login'
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
               # Remove the default error message
            form.errors.clear()
             
            # Custom error message for invalid login attempt
            messages.error(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'login'
        })





# register view

# class RegisterView(View):
#     template_name = 'register.html'

#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         form = UserCreationForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Registration failed.')
#         return render(request, self.template_name, {'form': form})



class RegisterView(View):
    template_name = 'auth.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserCreationForm()
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'register'
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Registration failed.')
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'register'
        })





# class CustomLogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('home')
    
    
    
    
class CustomLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have been logged out successfully.")
        return redirect('home')
    
    



def configure_car(request):
    
    return render(request, 'configure_car.html')


def about_us(request):
    return render(request, 'about_us.html')


