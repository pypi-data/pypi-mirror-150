from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='py_desc',
    version='0.5.2',
    packages=['py_desc/built_in'],
    url='https://github.com/syth0le/py_desc',
    long_description=long_description,
    license='Apache 2.0',
    author='Cherednichenko Daniil',
    author_email='syth0le565@gmail.com',
    description='A simple fields descriptors tool',
    python_requires='>=3.7.0',
    platforms=['all'],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
)