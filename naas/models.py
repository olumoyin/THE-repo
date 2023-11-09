from django.db import models
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# # Signals
# from django.dispatch import receiver
# from django.db.models.signals import post_save



class ServiceRequest(models.Model):
    ESTATE_TYPES = [
        ("multi dwelling unit", "Multi Dwelling Unit"),
        ("single unit", "Single Unit")
    ]
    SERVICE_TYPES = [
        ("GPON", "GPON"),
        ("P2P", "P2P"),
        ("WIFI", "WIFI"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Service type
    service = models.CharField(max_length=4, choices=SERVICE_TYPES)

    # Property infomation
    property_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    has_central_server_room = models.BooleanField(default=False)
    house_count = models.PositiveIntegerField(default=1)
    estate_type = models.CharField(max_length=20, choices=ESTATE_TYPES)
    request_contract = models.FileField(upload_to='naas/service-requests/request-contracts/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=False, null=False)
    
    # Request author contact
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField()
    
    # Metric
    is_fulfilled = models.BooleanField()




# @receiver(post_save, sender=ServiceRequest)
# def notify_admin_of_new_request(sender, instance, created, **kwargs):
#     if created:
#         try:
#             subject = "New NaaS Service Request\n"
#             body = f"""
#                 A request for a {instance.estate_type} estate  with {instance.house_count} house(s) has 
#                 been created.\n
#                 Property Name: {instance.property_name}\n
#                 Address: {instance.address}\n\n

#                 Contact: {instance.constant_info}
#             """
#             # Send email notification to info@wisptalkafrica.com
#             print(subject, body)
#         except Exception as e:
#             print(f'Error sending service request notification email: {e}')
        
