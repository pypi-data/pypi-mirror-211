from setuptools import setup

setup(
    name='logvinov-xmlJSON-serializer',
    version='0.1.0',
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
    author='Sinbanbon',
    author_email='',
    description=''
)
