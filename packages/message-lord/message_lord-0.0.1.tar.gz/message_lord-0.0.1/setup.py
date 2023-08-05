
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='message_lord',
    version='0.0.1',
    description='A very basic library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Lord',
    author_email='ramashisx@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='message',
    packages=find_packages(),
    install_requires=['']
)