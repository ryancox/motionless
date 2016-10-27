#!/usr/bin/python

__author__ = 'Ryan Cox <ryan.a.cox@gmail.com>'
__version__ = '1.3'

# Distutils version
METADATA = dict(
    name = "motionless",
    version = __version__,
    py_modules = ['setup', 'motionless'],
    author = 'Ryan Cox',
    author_email = 'ryan.a.cox@gmail.com',
    description = 'An easy way to generate Google Static Map URLs with Python.',
    license = 'Apache 2.0 License',
    url = 'http://github.com/ryancox/motionless',
    keywords = 'google static maps url api georss mapping gpx kml geo gis',
    test_suite='tests',
    tests_require=[],
)

# Setuptools version
SETUPTOOLS_METADATA = dict(
    install_requires = ['setuptools', 'six'],
    include_package_data = True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Internet',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)

def Main():
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)

if __name__ == '__main__':
    Main()
