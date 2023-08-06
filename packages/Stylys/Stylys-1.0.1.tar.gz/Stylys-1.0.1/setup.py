from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='Stylys',
    version='1.0.1',
    description='Just a next text styling library for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivulka',
    url='https://github.com/IvulkaCZ/Stylys',
    packages=['stylys'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)