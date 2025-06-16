# users/urls.py
from django.urls import path
from .views import contact_view, delete_message_ajax
from django.contrib.auth import views as auth_views
from .views import LoginView, RegisterView, CustomLogoutView, ProfileView

urlpatterns = [
    path('contact/', contact_view, name='contact_form'),
    path('delete-message/', delete_message_ajax, name='delete_message_ajax'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
    ), name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='view_profile'),
    
]