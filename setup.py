from setuptools import setup, find_packages

setup(
    name = 'django-timezones',
    version = '0.1',
    description = 'Timezone localization without any thinking or doing whatsoever.',
    long_description = open('README.md').read(),
    author = 'James Friedman',
    author_email = 'jamesmfriedman@gmail.com',
    url = 'https://github.com/jamesmfriedman/django-timezones/',
    download_url = 'https://github.com/jamesmfriedman/django-timezones/',
    license = 'Apache',
    keywords = ('timezone','tzinfo', 'datetime', 'jamesmfriedman', 'time', 'django', 'django-timezones'),
    packages = find_packages(),
    package_data = {'timezones': ['static/timezones/js/*']},
    tests_require = (
        'django>=1.4',
    ),
    include_package_data = True,
    zip_safe = False,  # because we're including media that Django needs
    install_requires = (
        'pytz',
    ),
)