from serie.models import Serie

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
    if request.method == "GET":
        if request.GET.has_key(u'query'):
            value = request.GET[u'query']
            model_results = Serie.objects.filter( Q(name_es__icontains=value) | Q(name__icontains=value))[:4]
            return  { 'results': model_results }

