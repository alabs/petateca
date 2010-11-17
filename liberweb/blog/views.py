from django.shortcuts import render_to_response
from blog.models import Post

def index(request):
    all_posts = Post.objects.all().order_by('-date')
    template_data = {'posts' : all_posts}
    # TODO return image
 
    return render_to_response('blog/get_post.html', template_data)

