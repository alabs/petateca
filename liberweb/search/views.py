from django.utils import simplejson
from django.http import HttpResponse
from liberweb.serie.models import Serie


def search_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 3
            if len(value) > 2:
                model_results = Serie.objects.filter(name__icontains=value)
                results = [ x.name for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
