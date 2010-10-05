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
    ]
)
