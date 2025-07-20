from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = 'Block an IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **kwargs):
        ip_address = kwargs['ip_address']
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f"IP address {ip_address} is already blocked."))
        else:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f"IP address {ip_address} has been blocked successfully."))
