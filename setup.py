#! coding=utf8
from distutils.core import setup

setup(
    name='django-admin-flexselect',
    version='0.4.0',
    author=u'Rune Kaagaard',
    author_email='rumi.kg@gmail.com',
    packages=['flexselect'],
    url='https://github.com/runekaagaard/django-admin-flexselect',
    license='Public Domain',
    description='Dynamic select fields for the Django Admin that just works.',
    long_description=open('README.markdown').read(),
    package_data={'flexselect': ['static/flexselect/js/flexselect.js']},
)
