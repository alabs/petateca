from django.utils import simplejson
from django.http import HttpResponse
from liberweb.serie.models import Serie


def search_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'query'):
            value = request.GET[u'query']
            # Ignore queries shorter than length 3
            if len(value) > 1:
                model_results = Serie.objects.filter(name__icontains=value)
                suggestions = [ str(x.name) for x in model_results ]
                #result = '{ query: %s, suggestions: %s }' % (value, suggestions)
    json = simplejson.dumps({'query': value, 'suggestions': suggestions, })
    return HttpResponse(json, mimetype='application/json')
