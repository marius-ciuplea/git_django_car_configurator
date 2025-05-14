from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
                    HomeView,
                    ConfigureCarModelView,
                    ConfigureView, 
                    # configure_car, 
                    about_us,
                    delete_configuration_ajax, 
                    send_offer_ajax
                )


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('configure/carousel', configure_car, name='configure_carousel'),
    path('configure/<int:car_id>/', ConfigureCarModelView.as_view(), name='configure_car'),
    path('configure/', ConfigureView.as_view(), name='configure_car_list'),
    path('about_us/', about_us, name='about-us'),
    path('delete-configuration/', delete_configuration_ajax, name='delete_configuration_ajax'),
    path('send-offer/', send_offer_ajax, name='send_offer_ajax'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


