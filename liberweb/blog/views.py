from django.shortcuts import render_to_response, get_object_or_404
from liberweb.blog.models import Post

def index(request):
    all_posts = Post.objects.all().order_by('-date')
    template_data = {'posts' : all_posts}
    # TODO return image
    return render_to_response('blog/post_list.html', template_data)


def get_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    imgs = post.images.all()[0]
    img_src = imgs.src if imgs else None
    return render_to_response('blog/get_post.html', {
        'post': post,
        'image': img_src,
    })
