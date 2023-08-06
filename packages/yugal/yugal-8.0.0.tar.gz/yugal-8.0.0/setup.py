from setuptools import setup, find_packages

setup(
    name='yugal',
    version='8.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'yugal=yugal:main',
        ],
    },
)
