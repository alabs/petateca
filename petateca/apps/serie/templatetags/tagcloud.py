from serie.models import Genre, Network
from book.models import Category, Author

from django import template
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('serie/tagcloud.html')
def tagcloud(tag_type, val_max, val_min):
    tagcloud = []
    val_max, val_min = int(val_max), int(val_min)
    if tag_type == 'Genre': object_list = Genre.objects.annotate(total=Count('series'))
    elif tag_type == 'Network': object_list = Network.objects.annotate(total=Count('series'))
    elif tag_type == 'Author': object_list = Author.objects.annotate(total=Count('books'))
    elif tag_type == 'Category': object_list = Category.objects.annotate(total=Count('books'))
    object_list = object_list.order_by('-total')
    for t in object_list:
        countdown = t.total
        if countdown > val_max: tag = "tag3"
        elif countdown > val_min < val_max: tag = "tag2"
        elif countdown < val_min: tag = "tag1" 
        else: tag = "tag1"
        tdict = {
            'tag': tag,
            'name': t.name,
            'slug_name': t.slug_name,
            'total': countdown,
        }
        if tag_type == 'Genre': tdict['class'] = 'genre'
        elif tag_type == 'Network': tdict['class'] = 'network'
        elif tag_type == 'Author': tdict['class'] = 'author'
        elif tag_type == 'Category': tdict['class'] = 'category'
        tagcloud.append(tdict)
    return { 'tagcloud_list' : tagcloud }
