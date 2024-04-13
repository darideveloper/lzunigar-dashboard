from django.urls import path
from contact_forms import views

urlpatterns = [
    path('', views.ContactForm.as_view(), name='contact_form'),
]
