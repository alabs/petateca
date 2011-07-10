from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from time import strftime, time, sleep
from voting.models import Vote
import logging

from apps.checker.utils.checker import Checker
from serie import models as m

logger = logging.getLogger(__name__)
link_ct = ContentType.objects.get(app_label="serie", model="link")
user = User.objects.get(username = settings.DEFAULT_USER_FOR_LINKS)


class ProcessLinks(object):

    def __init__(self):
        self.c_upvoted = 0
        self.c_already_upvoted = 0
        self.c_inactive = 0
        self.c_already_inactive = 0
        self.c_notvalid = 0
    
    def link_upvote(self, link):
        '''
        Try to upvote the received link
        '''
        try: 
            is_upvoted = Vote.objects.get(content_type = link_ct, object_id=link.id, user=user).is_upvote()
            if is_upvoted:
                logger.info('LINK: %s - %s | STATUS: already upvoted' % (link.id, link.url))
            self.c_already_upvoted = self.c_already_upvoted + 1
        except Vote.DoesNotExist:
            Vote.objects.record_vote(link, user, +1)
            logger.info('LINK: %s - %s | STATUS: upvoted' % (link.id, link.url))
            self.c_upvoted = self.c_upvoted + 1
        return True

    def link_inactivate(self, link):
        '''
        Change the boolean property is_active of the received link
        '''
        if link.is_active:
            link.is_active = False
            link.save()
            logger.info('LINK: %s - %s | STATUS: inactive' % (link.id, link.url))
            self.c_inactive = self.c_inactive + 1
        else: 
            logger.info('LINK: %s - %s | STATUS: already inactive' % (link.id, link.url))
            self.c_already_inactive = self.c_already_inactive + 1
        return True

    def process(self, link): 
        ''' 
        Recibe un link y teniendo en cuenta el OK o el KO de resultado de la URL,
        procede a deshabilitarla o a darle un +1 en las votaciones
        '''
        try: 
            link = m.Link.objects.get(id=link.id)
        except m.Link.DoesNotExist:
            logger.error('Link does not exist')
            return False
        checker = Checker()
        result = checker.get_status(link.url)
        link.check_date = datetime.now()
        link.save()
        if result == 'KO':
            self.link_inactivate(link)
        elif result == 'OK': 
            self.link_upvote(link)
        else:
            self.c_notvalid = self.c_notvalid + 1

    def timer_start(self, scan_type):
        '''
        Loggea y devuelve el tiempo de inicio en EPOCH.
        '''
        t_start = strftime("%a, %d %b %Y %H:%M:%S")
        i_start = time()
        logger.info('PROCESS LINKS - START CHECKING %s  - %s' % (scan_type, t_start))
        return i_start

    def timer_end(self, scan_type, i_start):
        '''
        Loggea y hace el calculo de inicio a fin en segundos.
        Tiene que recibir la hora de inicio en EPOCH.
        '''
        t_end = strftime("%a, %d %b %Y %H:%M:%S")
        i_end = time()
        segundos_raw = i_end - i_start
        segundos = int(str(segundos_raw).split('.')[0])
        if segundos < 60: 
            elapsed = '%s segundos' % (segundos)
        else: 
            minutos = segundos / 60
            elapsed = '%s minutos' % (minutos)
        logger.info('PROCESS LINKS - FINISHED CHECKING %s - %s' % (scan_type, t_end))
        logger.info('RESULTS')
        logger.info(' * Upvoted:            %s' % (self.c_upvoted))
        logger.info(' * Already Upvoted:    %s' % (self.c_already_upvoted))
        logger.info(' * Inactive:           %s' % (self.c_inactive))
        logger.info(' * Already Inactive:   %s' % (self.c_already_inactive))
        logger.info(' * Domain Not Valid:   %s' % (self.c_notvalid))
        logger.info('ELAPSED TIME: %s' % (elapsed))
        return True

    def countdown(self, selection, scan_type):
        ''' Aviso de cuantos links hay en la seleccion y posibilidad de cancelarlo '''
        count = selection.count()
        logger.info( "*" * 10 )
        if scan_type == 'DOWNVOTED':
            logger.info("Processing %s downvoted links" % (count))
            print "Processing %s downvoted links" % (count)
        elif scan_type == 'ALL':
            logger.info("Processing %s links" % (count))
            print "Processing %s links" % (count)
        print "Si quiere cancelarlo pulse CTRL + C"
        logger.info( "*" * 10 )
        for i in reversed(range(11)):
            sleep(1)
            print i

    def process_downvoted(self):
        '''
        Process the downvoted links
        '''
        downvotes = Vote.objects.all()
        self.countdown(downvotes, 'DOWNVOTED')
        i_start = self.timer_start('DOWNVOTED')
        for vote in downvotes:
            try:
                l = m.Link.objects.get(id=vote.object_id)
                if not l:
                    return False
                if not l.check_date or not l.check_date.isocalendar() == datetime.now().isocalendar():
                    # si ya fue checkeado hoy mismo, no lo hagamos de nuevo
                    self.process(l)
            except m.Link.DoesNotExist:
                vote.delete() 
                ERROR_STR = "DELETED - Vote ID %s (INEXISTING LINK)" % (vote.id)
                logger.error(ERROR_STR)
                return False
        self.timer_end('DOWNVOTED', i_start)

    def process_all_links(self):
        '''
        Process all the links
        '''
        all_links = m.Link.objects.all()
        self.countdown(all_links, 'ALL')
        i_start = self.timer_start('ALL')
        for l in all_links: 
            self.process(l)
        self.timer_end('ALL', i_start)
