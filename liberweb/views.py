from django.shortcuts import render_to_response
from liberweb.serie.models import Serie
from liberweb.blog.models import Post
from django.contrib import messages
from liberweb.decorators import render_to

@render_to('index.html')
def index(request):
    post_list = Post.objects.all().order_by('-date')[:3]
    post_list_2 = Post.objects.all().order_by('-date')[3:6]
    serie_list = Serie.objects.order_by('?')[:5] # ?=random
    if request.session.get('visited', False):
        return { 
                'posts': post_list, 
                'posts2': post_list_2, 
                'series': serie_list,
         }
    else:
        request.session['visited'] = True
        initial_message = 1
        return { 
                'posts': post_list, 
                'posts2': post_list_2, 
                'series': serie_list,
                'initial_message': initial_message,
         }
