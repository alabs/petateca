from voting.models import Vote

def order_links_by_vote(episode, limit=5):
   ''' 
   Receives an Episode instance, returns a dict with 5 best rated links by score.
   Example:
   >>> from lib.order_links_by_vote import order_links_by_vote 
   >>> serie = Serie.objects.get(name="True Blood")
   >>> season = Season.objects.get(season='1', serie=serie)
   >>> episode = Episode.objects.get(episode='1', season=season)
   >>> link_list = order_links_by_vote(episode)
   >>> print link_list
   [{'link': u'http://www.megaupload.com/?d=8ODSOMTO', 'score': 4, 'audio': u'en', 'sub': u'es', 'num_votes': 4}, {'link': u'http://www.megaupload.com/?d=IRXOISWO', 'score': 2, 'audio': u'es', 'sub': u'es', 'num_votes': 2}, {'link': u'http://www.megaupload.com/?d=05I3KULU', 'score': 0, 'audio': u'es', 'sub': u'es', 'num_votes': 0}, {'link': u'http://www.megaupload.com/?d=PRNEDP0O', 'score': 0, 'audio': u'es', 'sub': u'es', 'num_votes': 0}, {'link': u'http://www.megaupload.com/?d=F7VAXN40', 'score': 0, 'audio': u'es', 'sub': u'es', 'num_votes': 0}]
   ''' 
   linklist = []
   for l in episode.links.all():
       votesdict = Vote.objects.get_score(l)
       votesdict.update({'link': l.url, 'audio': l.audio_lang.iso_code})
       if l.subtitle:
           votesdict.update({'sub': l.subtitle.iso_code})
       linklist.append(votesdict)
   linklist = sorted(linklist, key= lambda k: k['score'])
   linklist.reverse()
   return linklist[0:limit]
