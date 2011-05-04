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

        visionado = ('megavideo')
        descarga = ('megaupload', 'gigasize', 'fileflyer', 'fileserve')
        torrent = ('torrent', 'bt-chat', 'mininova', 'torrage', 'zoink')

        if domain.startswith(visionado):
            domain_type = 'Visionado online'
        elif domain.startswith(descarga):
            domain_type = 'Descarga directa'
        elif domain.startswith(torrent):
            domain_type = 'Torrent'
        else:
            domain_type = 'Desconocido'
    except:
        domain_type = 'Desconocido'
    return domain_type
