from django.core.management import BaseCommand

from djangoratings.models import SimilarUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        SimilarUser.objects.update_recommendations()
