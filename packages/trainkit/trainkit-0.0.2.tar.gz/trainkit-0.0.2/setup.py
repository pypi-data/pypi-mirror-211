from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='trainkit',
    version='0.0.2',
    author='Enrique Mendez',
    author_email='enrique.phys@email.com',
    description='A library for simplifying training in Python',
    long_description=long_description,
    url='https://github.com/scholarlysalmons/trainkit',
    packages=find_packages(),
    install_requires=[
        'torch',
    ],
)
