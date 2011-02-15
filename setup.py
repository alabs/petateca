import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

setup(
    name="petateca",
    version='0.1dev',
    author="",
    author_email="",
    packages=['petateca',],
    url='',
    license='',
    description='Web de petateca',
    long_description=open('README.txt').read(),
    install_requires=[
        'django',
        'PIL',
        'docutils',
        'South>=0.7.3',
        'django-modeltranslation',
        'django-rosetta',
        'IMDbPY',
        'sorl-thumbnail>=11.01',
        'tvdb_api',
        'django-haystack',
        'Whoosh',
        'django-ratings',
        'django-registration',
        'django-voting',
        'django-taggit',
        'django-localeurl',
        'twitter',
        'simplejson',
        'django-avatar',
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
        "http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage",
    ],
)
