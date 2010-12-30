from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.filter()
@stringfilter
def extract_domain(value): # Only one argument.
    "Extract domain from url"
    domain = value.split('http://')[1].split('/')[0]
    if domain.startswith('www.'):
        domain = domain.replace('www.','')
    return domain 

