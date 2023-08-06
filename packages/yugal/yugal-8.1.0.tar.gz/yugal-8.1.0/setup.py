from setuptools import setup

setup(
    name='yugal',
    version='8.1.0',
    author='Paurush Sinha',
    author_email='stuff.random.in@gmail.com',
    description='Yugal CLI',
    py_modules=['yugal'],
    entry_points={
        'console_scripts': [
            'yugal = yugal:start',
        ],
    },
)
