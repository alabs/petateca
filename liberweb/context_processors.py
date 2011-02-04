from django.conf import settings # import the settings file


def site_name(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'SITE_NAME': settings.SITE_NAME}
