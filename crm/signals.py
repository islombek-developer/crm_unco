from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
from .models import Attendance

@receiver(post_save, sender=Attendance)
def send_absence_notification(sender, instance, created, **kwargs):
    if not instance.status:
        try:
            student = instance.student
            phone = student.phone  
            message = f"Hurmatli ota-ona, Sizning farzandingiz {student.full_name} {instance.date.date} kuni darsga kelmadi."
            
            send_sms_notification(phone, message)
        except Exception as e:
            print(f"SMS sending failed: {str(e)}")

def send_sms_notification(phone_number, message):
 
    auth_url = "https://notify.eskiz.uz/api/auth/login"
    auth_data = {
        "email": settings.ESKIZ_EMAIL,
        "password": settings.ESKIZ_PASSWORD
    }
    
    try:

        auth_response = requests.post(auth_url, json=auth_data)
        token = auth_response.json()['data']['token']
        
        sms_url = "https://notify.eskiz.uz/api/message/sms/send"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        sms_data = {
            "mobile_phone": phone_number,
            "message": message,
            "from": "4546"  
        }
        
        response = requests.post(sms_url, headers=headers, json=sms_data)
        return response.json()
        
    except Exception as e:
        raise Exception(f"SMS sending failed: {str(e)}")