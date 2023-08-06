from setuptools import find_packages, setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dashadmdv-custom-serializer',
    version='0.1.0',
    packages=find_packages(include=[str(this_directory)]),
    description='My lab for uni',
    author='dashadmdv',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
