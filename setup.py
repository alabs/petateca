import distribute_setup
distribute_setup.use_setuptools()

bla = 'hola mundo'

from setuptools import setup

setup(
    name="petateca",
    version='0.2dev',
    author="",
    author_email="",
    packages=['petateca',],
    url='',
    license=open('LICENSE').read(),
    description='Web de petateca',
    long_description=open('README.md').read(),
    install_requires=[
        'django',
        'South>=0.7.3',
        'django-modeltranslation',
        'sorl-thumbnail>=11.01',
        'django-haystack>=1.2.0',
        'Whoosh',
        'django-voting',
        'django-avatar',
        'django-rosetta',
        'django-indexer',
        'django-paging',
        'django-sentry',
        'django-compress',
        'django-endless-pagination',
        'django-generic-aggregation',
        'unittest2',
        'python-twitter',
        'django-memcache-status',
        'django-celery',
        'django-axes',
        #'django-blog-zinnia',
        #'django-bitly',
        #'django-piston', lo instalamos a traves de src/ por ser este fork
        # https://bitbucket.org/joeb/django-piston/
        #'django-ratings',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
    dependency_links = [
        #XXX: For django-modeltranslation
        "https://github.com/Fantomas42/django-blog-zinnia.git#egg=django-blog-zinnia-0.8.1",
        "http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage",
    ],
)
