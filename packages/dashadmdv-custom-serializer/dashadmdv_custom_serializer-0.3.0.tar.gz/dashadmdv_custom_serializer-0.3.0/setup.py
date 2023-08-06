from setuptools import find_packages, setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dashadmdv_custom_serializer',
    version='0.3.0',
    packages=['custom_serializer',
              'custom_serializer.encoder',
              'custom_serializer.serializers'],
    description='My lab for uni',
    author='dashadmdv',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
