from django.core.management.base import BaseCommand
from mailings.models import Mailing
from mailings.services import send_mailing


class Command(BaseCommand):
    help = 'Send a mailing to all recipients.'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        mailing = Mailing.objects.get(id=mailing_id)
        send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS(f'Mailing {mailing_id} sent successfully.'))