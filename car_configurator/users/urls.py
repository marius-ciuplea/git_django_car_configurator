# users/urls.py
from django.urls import path
from .views import view_profile, contact_view, delete_message_ajax
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('profile/', view_profile, name='view_profile'), 
    path('contact/', contact_view, name='contact_form'),
    path('delete-message/', delete_message_ajax, name='delete_message_ajax'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        
    ), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),
    
]