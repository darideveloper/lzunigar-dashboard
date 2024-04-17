import os
from django.views import View
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.core import mail
from contact_forms import models
from lzunigar_dashboard import settings
from dotenv import load_dotenv

# Env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")


@method_decorator(csrf_exempt, name='dispatch')
class ContactForm(View):
    
    def post(self, request):
        """ Send email and redirect """

        # Get form data
        form_data = request.POST.dict()

        # Check requited inputs
        inputs_names = ["api_key", "form"]
        for input_name in inputs_names:
            if input_name not in form_data.keys():
                return JsonResponse({
                    "status": "error",
                    "message": f"missing {input_name} input",
                    "data": {}
                }, status=400)
        
        # Get form model and validate
        form_name = form_data["form"]
        model = models.models_relation.get(form_name, None)
        if not model:
            return JsonResponse({
                "status": "error",
                "message": "invalid form",
                "data": {}
            }, status=400)
        
        # Validate api user name
        if not form_data["api_key"] == API_KEY:
            return JsonResponse({
                "status": "error",
                "message": "invalid login",
                "data": {}
            }, status=401)
        
        # Get and validate model fields
        model_fields = models.GanoConCocaCola._meta.get_fields()
        model_fields_names = [field.name for field in model_fields]
        model_fields_names = list(filter(
            lambda field: field not in [
                "id",
                "created_at",
                "updated_at",
                "redirect",
                "api_key"
            ],
            model_fields_names
        ))
        for field_name in model_fields_names:
            if field_name not in form_data.keys() or not form_data[field_name]:
                return JsonResponse({
                    "status": "error",
                    "message": f"missing '{field_name}' field",
                    "data": {}
                }, status=400)
            
        # Save form data
        fields_data = {}
        for model_field_name in model_fields_names:
            fields_data[model_field_name] = form_data[model_field_name]
        model(**fields_data).save()
            
        # Connect to email server
        connection = mail.get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_ssl=settings.EMAIL_USE_SSL
        )
        connection.open()
        
        # Create email
        fields_data_text = ""
        for field_name, field_value in fields_data.items():
            fields_data_text += f"{field_name}: {field_value}\n"
        model_admin_url = f"{settings.HOST}/admin/contact_forms/{form_name}/"
        subject = "Nuevo lead en tu dashboard"
        message = f"Accede a {model_admin_url} para ver " \
            f"el nuevo lead\n{fields_data_text}"
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_TO]
        )

        # Send email
        email.connection = connection
        email.send(
            fail_silently=False
        )
        
        connection.close()
        
        # Redirect or send response
        redirect = form_data.get("redirect", "")
        if redirect:
            return HttpResponseRedirect(form_data["redirect"])
        else:
            return JsonResponse({
                "status": "success",
                "message": "email sent",
                "data": {}
            }, status=200)