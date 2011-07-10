'''
    Busca los links y los procesa (deshabilitar o darle un +1)
'''

from apps.checker.utils.process_links import ProcessLinks
from django.core.management.base import BaseCommand, CommandError
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '[actions ...]'
    help = '''
    Check and process the given links. 
    If the link is valid, it gets a +1 in voting. 
    If the link is invalid, it gets deactivated (not listed while listing links)

    Possible actions are 'all' and 'downvoted'. Example of use: 

    $ ./manage.py checker all
    $ ./manage.py checker downvoted
    '''

    def handle(self, *args, **options):
        if 'all' in args:
            process = ProcessLinks()
            process.process_all_links()
        elif 'downvoted' in args:
            process = ProcessLinks()
            process.process_downvoted()
        else:
            raise CommandError('%s is not a valid option' % (args[0]))




