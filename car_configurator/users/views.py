from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, ProfilePictureForm, ContactFormForm
from .models import Profile, ContactForm
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Configuration


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
            messages.success(request, 'Logged in successfully', extra_tags='success-message')
            return redirect('home')
        else:
               # Remove the default error message
            form.errors.clear()
            messages.error(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.',  extra_tags='error-message')
            
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'login'
        })



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
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Registration failed', extra_tags='error-message')
        return render(request, self.template_name, {
            'form': form,
            'form_type': 'register'
        })

    
    
class CustomLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have been logged out successfully.",  extra_tags='success-message')
        return redirect('home')




class ProfileView(LoginRequiredMixin, View):
    template_name = 'view_profile.html'

    def get(self, request):
        try:
            profile, _ = Profile.objects.get_or_create(user=request.user)
        except Exception:
            return redirect('register')

        edit_mode = request.GET.get("edit") == "true"
        
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfilePictureForm(instance=profile)
        user_messages = ContactForm.objects.filter(user=request.user).order_by('-created_at')
        
        saved_configs = Configuration.objects.filter(user=request.user, offered_config=False).order_by('-created_at')
        offered_configs = Configuration.objects.filter(user=request.user, offered_config=True).order_by('-created_at')

        context = {
            'profile': profile,
            'edit_mode': edit_mode,
            'user_form': user_form,
            'profile_form': profile_form,
            'user_messages': user_messages,
            'saved_configs': saved_configs,
            'offered_configs': offered_configs,
            'has_saved_configs': saved_configs.exists(),
            'has_offered_configs': offered_configs.exists(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            profile, _ = Profile.objects.get_or_create(user=request.user)
        except Exception:
            return redirect('register')

        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!', extra_tags='success-message')
            return redirect('view_profile')

        # If invalid, re-render the page with existing configs and forms
        user_messages = ContactForm.objects.filter(user=request.user).order_by('-created_at')
        saved_configs = Configuration.objects.filter(user=request.user, offered_config=False).order_by('-created_at')
        offered_configs = Configuration.objects.filter(user=request.user, offered_config=True).order_by('-created_at')

        context = {
            'profile': profile,
            'edit_mode': True,
            'user_form': user_form,
            'profile_form': profile_form,
            'user_messages': user_messages,
            'saved_configs': saved_configs,
            'offered_configs': offered_configs,
            'has_saved_configs': saved_configs.exists(),
            'has_offered_configs': offered_configs.exists(),
        }
        return render(request, self.template_name, context)


def contact_view(request):
    form = ContactFormForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            local_created_time = contact.created_at.astimezone(timezone.get_current_timezone())
            return JsonResponse({
                'success': True,
                'created': local_created_time.strftime('%Y-%m-%d %H:%M:%S'),
                'message': contact.message
            })
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    return render(request, 'contact.html', {'form': form})


@require_POST
@login_required
def delete_message_ajax(request):
    message_id = request.POST.get('message_id')
    message = get_object_or_404(ContactForm, id=message_id, user=request.user)
    message.delete()
    return JsonResponse({'success': True})



