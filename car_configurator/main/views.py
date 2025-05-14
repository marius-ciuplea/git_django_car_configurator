from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import CarModel, Engine, Color, Wheel, Configuration
from .forms import ConfigurationForm
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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


# Configure cars 
class ConfigureCarModelView(View):
    def get(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        config = Configuration.objects.filter(car_model=car, user=request.user).last()
        
        if config:
            form = ConfigurationForm(instance=config, car_model=car)
        
        else:
            form = ConfigurationForm(car_model=car)
            

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car),
            'existing_config_id': config.id if config else None
        })

    def post(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        config_id = request.POST.get("config_id")
        action = request.POST.get("action")
        
        if config_id:
            #Update
            configuration = get_object_or_404(Configuration, id=config_id, user=request.user)
            form = ConfigurationForm(request.POST, instance=configuration, car_model=car)
        
        else:
            # Create
            form = ConfigurationForm(request.POST, car_model=car)  
            

        if form.is_valid():
            configuration = form.save(commit=False)
            configuration.car_model = car
            configuration.user = request.user
            configuration.saved_config = True
            
            
            if action == "send_offer":
                configuration.offered_config = True
                messages.success(request, "The offer has been sent successfully!")
                
            elif action == "save":
                configuration.offered_config = False
                messages.success(request, "Your configuration has been saved!")
                
            configuration.save()
            return redirect('view_profile')  # Redirect after saving the configuration

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car),
            'config_id': config_id
        })
        


# def configure_car(request):
#     colors = Color.objects.all()
#     return render(request, 'configure_car.html', {'colors': colors})


def about_us(request):
    return render(request, 'about_us.html')


def update_config(request, config_id):
    config = get_object_or_404(Configuration, id=config_id, user=request.user)
    car_model = config.car_model
    
    if request.method == 'POST':
        form = ConfigurationForm(request.POST, instance=config, car_model=car_model)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ConfigurationForm(instance=config, car_model=car_model)
    
    return render(request, 'update_config.html', {'form':form, 'config':config})


@require_POST
@login_required
def delete_configuration_ajax(request):
    config_id = request.POST.get('config_id')
    config = get_object_or_404(Configuration, id=config_id, user=request.user)
    config.delete()
    return JsonResponse({'success': True})



@login_required
@require_POST
def send_offer_ajax(request):
    config_id = request.POST.get('config_id')

    if not config_id:
        return JsonResponse({'success': False, 'error': 'Missing config ID'})

    try:
        config = Configuration.objects.get(id=config_id, user=request.user)
        config.offered_config = True
        config.save()
        return JsonResponse({'success': True})
    except Configuration.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Configuration not found'})