from serie.models import Genre, Network
from django import template

register = template.Library()


@register.inclusion_tag('serie/tagcloud.html')
def tagcloud(tag_type, val_max, val_min):
    tagcloud = []
    val_max, val_min = int(val_max), int(val_min)
    if tag_type == 'Genre': object_list = Genre.objects.select_related('serie').all()
    elif tag_type == 'Network': object_list = Network.objects.all()
    for t in object_list:
        countdown = t.series.count()
        if countdown > val_max: tag = "tag3"
        elif countdown > val_min < val_max: tag = "tag2"
        elif countdown < val_min: tag = "tag1" 
        else: tag = "tag1"
        tdict = {
            'tag': tag,
            'name': t.name,
            'slug_name': t.slug_name
        }
        if tag_type == 'Genre': tdict['class'] = 'genre'
        elif tag_type == 'Network': tdict['class'] = 'network'
        tagcloud.append(tdict)
    return { 'tagcloud_list' : tagcloud }
