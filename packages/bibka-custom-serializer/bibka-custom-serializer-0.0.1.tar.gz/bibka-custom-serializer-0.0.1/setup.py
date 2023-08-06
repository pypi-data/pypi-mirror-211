from setuptools import setup

setup(
    name='bibka-custom-serializer',
    version='0.0.1',
    packages=['custom_serializer',
              'custom_serializer.encoder',
              'custom_serializer.serializers'],
    entry_points={
        "console_scripts": [
            "custom-serialize = custom_serializer.custom_serializer:main"
        ]
    },
    url='',
    license='',
    author='BibkaIgor',
    author_email='',
    description=''
)
