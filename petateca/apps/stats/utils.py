# coding=utf-8
'''
COMO FUNCIONA
Crear un script asi:

from stats.utils import add_stats

all_types = [ 'chart_users', 'chart_series', 'chart_links', 'chart_seasonlinks', 'chart_book',
'chart_booklink', 'chart_vote', 'chart_rating', ]

for t in all_types: add_stats(t)
'''
from django.contrib.contenttypes.models import ContentType

from stats.models import StatType

def batch_update_stats(model, total=None):
    '''
    Save content_type and total count of a given Model - helper 
    Si no le pasamos un valor para count es que es la suma de ese modelo mismamente
    Es para diferenciar por ejemplo entre todos los links y todos los links activos
    TODO get stattype and apply item
    '''
    # Get the instance's content type
    ctype = ContentType.objects.get_for_model(model)
    st = StatType.objects.get(content_type=ctype)
    if not total: total = model.objects.count()
    st.statitem_set.create(total=total)


def initial_stats(model, description, chart_div):
    ''' Helper para que sea mas facil crear los tipos de estadisticas '''
    ctype = ContentType.objects.get_for_model(model)
    StatType.objects.create(
        content_type=ctype,
        description=description,
        chart_div=chart_div,
    )


def create_initial_stats():
    from django.contrib.auth.models import User
    from apps.serie.models import Serie, Link, LinkSeason
    from apps.book.models import Book, BookLink
    from voting.models import Vote
    from djangoratings.models import Vote as Rating
    initial_stats(User, 'Usuarios registrados', 'chart_users')
    initial_stats(Serie, 'Series creadas', 'chart_series')
    initial_stats(Link, 'Enlaces agregados a episodios', 'chart_links')
    initial_stats(LinkSeason, 'Enlaces agregados a temporadas', 'chart_seasonlinks')
    initial_stats(Book, 'Libros creados', 'chart_book')
    initial_stats(BookLink, 'Enlaces agregados a libros', 'chart_booklink')
    initial_stats(Vote, 'Links votados', 'chart_vote')
    initial_stats(Rating, 'Series y libros valorados', 'chart_rating')

