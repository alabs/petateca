import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

setup(
    name="liberweb",
    version='0.1dev',
    author="",
    author_email="",
    packages=['liberweb',],
    url='',
    license='',
    description='Web de libercopy',
    long_description=open('README.txt').read(),
    install_requires=[
        'django',
        'PIL',
        'docutils',
        'South',
        'django-modeltranslation',
        'django-rosetta',
        'IMDbPY',
        'sorl-thumbnail',
        'tvdb_api',
        'django-haystack',
        'Whoosh',
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
