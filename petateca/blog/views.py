from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from blog.models import Post
from decorators import render_to
from taggit.models import Tag


@render_to('blog/post_list.html')
def index(request):
    all_posts = Post.objects.all().order_by('-date')
    all_tags = Post.tags.all()
    paginator = Paginator(all_posts, 3)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        post_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        post_list = paginator.page(paginator.num_pages)

    return {
        'posts': post_list,
        'all_posts': all_posts,
        'tags': all_tags,
    }


@render_to('blog/get_post.html')
def get_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    imgs = post.images.all()
    img_src = imgs[0].src if imgs else None
    tag_list = post.tags.all()
    return {
        'post': post,
        'image': img_src,
        'tag_list': tag_list,
    }


@render_to('blog/get_tag.html')
def get_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts_tagged = tag.taggit_taggeditem_items.all()
    return {
        'object_list': posts_tagged,
        'tag': tag,
    }
