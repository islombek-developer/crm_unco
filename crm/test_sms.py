from django.core.management.base import BaseCommand
from .models import Attendance
from crm.signals import send_sms_notification

class Command(BaseCommand):
    help = 'Test SMS sending functionality'

    def handle(self, *args, **options):
        try:
            phone = "+998900000000"
            message = "This is a test SMS message"
            
            response = send_sms_notification(phone, message)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent test SMS: {response}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send SMS: {str(e)}')
            )