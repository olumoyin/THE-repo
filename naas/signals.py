from django.dispatch import receiver
from django.db.models.signals import post_save

from naas.models import ServiceRequest


@receiver(post_save, sender=ServiceRequest)
def notify_admin_of_new_request(sender, instance, created, **kwargs):
    if created:
        try:
            subject = "New NaaS Service Request\n"
            body = f"""
                A request for a {instance.estate_type} estate  with {instance.house_count} house(s) has 
                been created.\n
                Property Name: {instance.property_name}\n
                Address: {instance.address}\n\n

                Contact: {instance.constant_info}
            """
            # Send email notification to info@wisptalkafrica.com
            print(subject, body)
        except Exception as e:
            print(f'Error sending service request notification email: {e}')
        
