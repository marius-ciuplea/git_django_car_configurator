from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import CarModel, Engine, Color, Wheel, Configuration
from .forms import ConfigurationForm
from django.contrib import messages
from django.utils import timezone

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

class CreateConfigurationView(View):
    def get(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        form = ConfigurationForm(car_model=car)
        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car)
        })

    def post(self, request, car_id):
        car = get_object_or_404(CarModel, id=car_id)
        form = ConfigurationForm(request.POST, car_model=car)
        
        if form.is_valid():
            config = form.save(commit=False)
            config.car_model = car
            config.user = request.user
            config.saved_config = True

            if request.POST.get("action") == "send_offer":
                config.offered_config = True
                config.offered_at = timezone.now()
                messages.success(request, "The offer has been sent successfully!",  extra_tags='success-message')
            else:
                config.offered_config = False
                config.offered_at = None
                messages.success(request, "Your configuration has been saved!",  extra_tags='success-message')

            config.save()
            return redirect('view_profile')

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car)
        })
        
        
        
class UpdateConfigurationView(View):
    def get(self, request, config_id):
        configuration = get_object_or_404(Configuration, id=config_id, user=request.user)
        car = configuration.car_model
        form = ConfigurationForm(instance=configuration, car_model=car)

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car),
            'config_id': config_id
        })

    def post(self, request, config_id):
        configuration = get_object_or_404(Configuration, id=config_id, user=request.user)
        car = configuration.car_model
        form = ConfigurationForm(request.POST, instance=configuration, car_model=car)

        if form.is_valid():
            config = form.save(commit=False)
            
            if request.POST.get("action") == "send_offer":
                config.offered_config = True
                config.offered_at = timezone.now()
                messages.success(request, "The offer has been sent successfully!",  extra_tags='success-message')
            else:
                config.offered_config = False
                config.offered_at = None
                messages.success(request, "Your configuration has been updated!",  extra_tags='success-message')

            config.saved_config = True
            config.save()
            return redirect('view_profile')

        return render(request, 'configure_car.html', {
            'car': car,
            'form': form,
            'colors': Color.objects.filter(car_model=car),
            'engines': Engine.objects.filter(car_model=car),
            'wheels': Wheel.objects.filter(car_model=car),
            'config_id': config_id  # 👈 same here
        })


def about_us(request):
    return render(request, 'about_us.html')


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
        config.offered_at = timezone.now()
        config.save()
        
        return JsonResponse({'success': True})
    except Configuration.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Configuration not found'})
    