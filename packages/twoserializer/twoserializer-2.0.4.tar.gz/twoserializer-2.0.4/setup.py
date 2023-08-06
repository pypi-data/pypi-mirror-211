from setuptools import setup

setup(
    name='twoserializer',
    version="2.0.4",
    description="serializer of few formats",
    author="Eb1geil",
    author_email='ksanvei03@gmail.com',
    url='https://github.com/Eb1geil/twoserializer',
    install_requires=["pytomlpp", 'pyyaml'],
    packages=['lab3'],
    test_suite='tests/',
)
