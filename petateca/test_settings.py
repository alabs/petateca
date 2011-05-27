from settings import *

import os

if os.uname()[1] == 'lalala':
    INSTALLED_APPS += ('django_hudson',)

