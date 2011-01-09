try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='projescape-web',
    version='0.1',
    description='a web site called projescape',
    author='Projescape Team',
    author_email='',
    url='http://projescape.lighthouseapp.com/',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.6",
        "Redis>=2.2.0",
        "recaptcha-client>=1.0.5",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'projescapeweb': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'projescapeweb': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = projescapeweb.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
