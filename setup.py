from setuptools import setup
setup(
    name='Open-GHX',
    version='0',
    author="Matt Mitchell",
    author_email="mitchute@gmail.com",
    packages=['ghx', ],
    long_description=open('README.md').read(),
    test_suite='nose.collector',
    tests_require=['nose'],
)
