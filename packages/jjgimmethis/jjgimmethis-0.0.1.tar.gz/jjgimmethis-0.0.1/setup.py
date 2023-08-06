from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='jjgimmethis',
    version='0.0.1',
    description='A module for generating random usernames, passwords, names and objects.',
    long_description=open('README.txt').read() + '\n\n\n' +
    open('CHANGELOG.txt').read(),
    url='https://github.com/jad-e/jjgimmethis',
    author='Khoo Hui Ying',
    author_email='khoohuiying01@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='random, generator, username, password, name, objects',
    packages=find_packages(),
    install_requires=['']
)
