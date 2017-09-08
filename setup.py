from distutils.core import setup

setup (
    name='wordsearch',
    version='0.9.0',
    py_modules=['engine', 'main', 'words'],

    # metadata
    author = 'Kurt Schallitz',
    author_email = 'kurt.schallitz@gmail.com',
    description='A program to generate simple wordsearch grids.',
    license='Public Domain',
    keywords='wordsearch'
)