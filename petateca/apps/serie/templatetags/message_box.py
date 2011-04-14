from django import template

register = template.Library()

@register.inclusion_tag('message_box.html')
def message_box(token):
    return {'message': token}
