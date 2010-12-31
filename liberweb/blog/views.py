from django.shortcuts import get_object_or_404
from liberweb.blog.models import Post

from liberweb.decorators import render_to

@render_to('blog/post_list.html')
def index(request):
    all_posts = Post.objects.all().order_by('-date')
    template_data = {'posts' : all_posts}
    return template_data

@render_to('blog/get_post.html')
def get_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    imgs = post.images.all()[0]
    img_src = imgs.src if imgs else None
    tag_list = post.tags.all()
    return {
        'post': post,
        'image': img_src,
        'tag_list': tag_list,
    }
