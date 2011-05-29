# encoding: utf-8
from django import template
#from django.utils.translation import ugettext_lazy as _
#TODO: i18n

register = template.Library()


@register.filter()
def echo_language(lang):  # Only one argument.
    "Converts iso_code to language name"
    if lang == 'es' or lang == 'es-es': lang_name = 'Español'
    elif lang == 'en': lang_name = 'Inglés'
    elif lang == 'eu': lang_name = 'Euskera'
    elif lang == 'ca': lang_name = 'Catalán'
    elif lang == 'jp': lang_name = 'Japonés'
    else: 
        lang_name = 'Desconocido'
    return lang_name
