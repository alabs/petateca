from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter()
@stringfilter
def extract_domain(value):  # Only one argument.
    "Extract domain from url"
    domain = "WRONG URL???"
    try:
        domain = value.split('http://')[1].split('/')[0]
        if domain.startswith('www.'):
            domain = domain.replace('www.', '')
    except:
        try:
            domain = value.split('https://')[1].split('/')[0]
            if domain.startswith('www.'):
                domain = domain.replace('www.', '')
        except:
            domain = "WRONG URL???"
    return domain
