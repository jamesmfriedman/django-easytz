from setuptools import setup, find_packages

setup(
    name = 'django-easytz',
    version = '0.2',
    description = 'Timezone localization without any thinking or doing whatsoever.',
    long_description = open('README.md').read(),
    author = 'James Friedman',
    author_email = 'jamesmfriedman@gmail.com',
    url = 'https://github.com/jamesmfriedman/django-easytz/',
    download_url = 'https://github.com/jamesmfriedman/django-easytz/',
    license = 'Apache',
    keywords = ('timezone','tzinfo', 'datetime', 'jamesmfriedman', 'time', 'django', 'django-timezones', 'django-tz', 'django-easytz'),
    packages = find_packages(),
    package_data = {'easytz': ['static/easytz/js/*']},
    tests_require = (
        'django>=1.4',
    ),
    include_package_data = True,
    zip_safe = False,  # because we're including media that Django needs
    install_requires = (
        'pytz',
    ),
)