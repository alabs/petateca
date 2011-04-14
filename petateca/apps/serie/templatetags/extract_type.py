from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter()
@stringfilter
def extract_type(value):  # Only one argument.
    "Extract type from url"
    domain_type = 'Desconocido'
    try:
        domain = value.split('http://')[1].split('/')[0]
        if domain.startswith('www.'):
            domain = domain.replace('www.', '')

        if domain.startswith('megavideo.com'):
            domain_type = 'Visionado Online'
        elif domain.startswith('megaupload.com') or domain.startswith('gigasize'): # or domain.startswith('fileflyer'):
            domain_type = 'Descarga Directa'
        elif domain.startswith('torrent') or domain.startswith('bt-chat') or domain.startswith('mininova'):
            domain_type = 'Torrent'
        else:
            domain_type = 'Desconocido'
    except:
        domain_type = 'Desconocido'
    return domain_type
