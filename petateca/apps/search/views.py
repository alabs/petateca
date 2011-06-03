from serie.models import Serie
from django.http import HttpResponse, HttpResponseBadRequest

from django.utils.simplejson import dumps
from django.db.models import Q
from decorators import render_to

@render_to('search/ajax_search.html')
def search_lookup(request):
    ''' 
    Busqueda en AJAX con jQuery 
    Se siguio este tutorial: http://www.marcofolio.net/webdesign/a_fancy_apple.com-style_search_suggestion.html
    (Adaptandolo a django)

    TODO: Agregarle navegacion con teclado: http://www.johnboy.com/blog/tutorial-instant-search-with-arrow-key-navigation-using-jquery-and-php

    Escupe los resultados en este formato:

    <p id="searchresults">
       <span class="category">[CATEGORY_FROM_DATABASE]</span>
          <a href="[URL_FROM_DATABASE]">
             <img alt="" src="search_images/[IMG_FROM_DATABASE]"/>
             <span class="searchheading">[HEADING_FROM_DATABASE]</span>
             <span>[TEXT_FROM_DATABASE]</span>
          </a>
          <a href="[URL_FROM_DATABASE]">
             <img alt="" src="search_images/[IMG_FROM_DATABASE]"/>
             <span class="searchheading">[HEADING_FROM_DATABASE]</span>
             <span>[TEXT_FROM_DATABASE]</span>
          </a>
          <!-- more items -->
       <span class="category">Webdesign</span>
          <a href="[URL_FROM_DATABASE]">
             <img alt="" src="search_images/[IMG_FROM_DATABASE]"/>
             <span class="searchheading">[HEADING_FROM_DATABASE]</span>
             <span>[TEXT_FROM_DATABASE]</span>
          </a>
       <!-- more categories -->
       <span class="seperator">
          <a href="http://www.marcofolio.net/sitemap.html">Nothing interesting here? Try the sitemap.</a>
       </span>
    </p>
    '''
    if request.GET.has_key(u'query'):
        value = request.GET[u'query']
        model_results = Serie.objects.filter( Q(name_es__icontains=value) | Q(name__icontains=value))[:4]
        return  { 'results': model_results }


def opensearch_lookup(request):
    ''' 
    Ajax sugestion/autocomplete para OpenSearch
    http://hublog.hubmed.org/archives/001681.html
    '''
    value = request.GET[u'q']
    if value:
        model_results = Serie.objects.filter(
                Q(name_es__icontains=value)
                | Q(name__icontains=value)
            ).values('name')
        list_model = [result['name'] for result in model_results]
        # El formato de respuesta debe ser asi: 
        # $ curl "http://suggestqueries.google.com/complete/search?output=firefox&q=opensear"
        # ["opensear",["opensearch","opensearchdescription","opensearch.xml"]]
        result = "[%s, %s]" % (dumps(value), dumps(list_model))
        return HttpResponse(result, mimetype='application/json')
    else:
        return HttpResponseBadRequest()
