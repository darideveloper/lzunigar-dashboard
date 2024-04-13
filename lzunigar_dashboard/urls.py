from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='admin/')),
    path('admin/', admin.site.urls),
    path('contact-form/', include('contact_forms.urls')),
]
