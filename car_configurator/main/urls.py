from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView, ConfigureCarModelView,
    LoginView, RegisterView, CustomLogoutView,ConfigureView
)

from . import views


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('configure/carousel', views.configure_car, name='configure_carousel'),
    path('configure/<int:car_id>/', ConfigureCarModelView.as_view(), name='configure_car'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('configure/', ConfigureView.as_view(), name='configure_car_list'),
    path('about_us/', views.about_us, name='about-us'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


