from django.contrib.auth.models import User
from serie.models import Serie, Link, LinkSeason
from book.models import Book, BookLink
from voting.models import Vote
from djangoratings.models import Vote as Rating

from django.core.management.base import BaseCommand

from stats.utils import batch_update_stats


class Command(BaseCommand):
    help = 'Passes trough a model list to save new streams (Statistics)'

    def handle(self, *args, **options):
      model_list = [ User, Serie, Link, LinkSeason, Book, BookLink, Vote, Rating ]
      for model in model_list:
         batch_update_stats(model)
         self.stdout.write('Registered streams for "%s"\n' % model)
