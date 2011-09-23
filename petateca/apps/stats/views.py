from django.contrib.contenttypes.models import ContentType
from core.decorators import render_to
from stats.models import StatType


@render_to('stats/statistics.html')
def show_stats(request):
    ''' 
    model depende de cual modelo estemos buscando, por ejemplo:
    user, serie, link, linkseason, book, booklink, vote, rating

    for m in model_list:
        ct = ContentType.objects.get_for_model(m)
        print ct.model
    '''
    stats = ['user', 'serie', 'link', 'linkseason', 'book', 'booklink']
    all_stats = {}
    for s in stats:
        ctype = ContentType.objects.get(model=s)
        st = StatType.objects.get(content_type=ctype)
        stats = st.statitem_set.all()
        all_stats[s] = stats 
    print all_stats
    return {
        'all_streams': all_stats,
    }


