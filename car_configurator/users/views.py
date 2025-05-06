from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, ProfilePictureForm, ContactFormForm
from .models import Profile, ContactForm
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST


@login_required
def view_profile(request):
    # Try to get or create the Profile, fallback if error
    try:
        profile, _ = Profile.objects.get_or_create(user=request.user)
    except Exception:
        profile = None

    edit_mode = request.GET.get("edit") == "true"

    if request.method == "POST":
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
           
            user.save()
            profile_form.save()

            return redirect('view_profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfilePictureForm(instance=profile)
    user_messages =ContactForm.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'profile': profile,
        'edit_mode': edit_mode,
        'user_form': user_form,
        'profile_form': profile_form,
        'user_messages':user_messages,
    }

    return render(request, 'view_profile.html', context)


# # Profile Update View
# class ProfileUpdateView(UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'users/update_profile.html'
#     success_url = reverse_lazy('view_profile')  # Redirect after successful update

#     def get_object(self):
#         # Get the Profile object for the logged-in user
#         return get_object_or_404(Profile, user=self.request.user)

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