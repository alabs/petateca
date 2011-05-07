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
    license=open('LICENSE').read(),
    description='Web de petateca',
    long_description=open('README.md').read(),
    install_requires=[
        'django',
        'South>=0.7.3',
        'django-modeltranslation',
        'sorl-thumbnail>=11.01',
        'django-haystack',
        'Whoosh',
        'django-ratings',
        'django-voting',
        'django-avatar',
        'django-rosetta',
        'django-piston',
        'django-indexer',
        'django-paging',
        'django-sentry',
        'django-compress',
        'unittest2',
      #  'docutils',
      #  'django-localeurl',
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
