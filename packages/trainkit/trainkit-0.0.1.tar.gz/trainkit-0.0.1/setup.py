from setuptools import setup, find_packages

setup(
    name='trainkit',
    version='0.0.1',
    author='Enrique Mendez',
    author_email='enrique.phys@email.com',
    description='A library for simplifying training in Python',
    packages=find_packages(),
    install_requires=[
        'torch',
    ],
)
