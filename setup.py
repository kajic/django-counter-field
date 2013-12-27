import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-counter-field',
    version='0.2',
    packages=find_packages(exclude=['tests']),
    license='MIT License',
    description='django-counter-field makes it extremely easy to denormalize and keep track of related model counts.',
    long_description=README,
    url='http://github.com/kajic/django-counter-field',
    author='Robert Kajic',
    author_email='robert@kajic.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-model-changes>=0.15',
    ],
    test_suite='runtests.runtests',
    tests_require=[
        'pysqlite',
        'django'
    ],
    zip_safe=False,
)
