class ImdbRouter(object):
    """A router to control all database operations on models in
    the imdblocal application"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'imdblocal':
            return 'imdb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'imdblocal':
            return 'imdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'imdblocal' or obj2._meta.app_label == 'imdblocal':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'imdb':
            return model._meta.app_label == 'imdblocal'
        elif model._meta.app_label == 'imdblocal':
            return False
        return None
