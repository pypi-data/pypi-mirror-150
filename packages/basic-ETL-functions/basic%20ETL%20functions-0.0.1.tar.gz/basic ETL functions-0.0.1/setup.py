from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='basic ETL functions',
    version='0.0.1',
    description='Contains functions that help in the geocoding, formating, and creating points and services portfolios.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abhinav Agrawal',
    author_email='abhinav.agrawal@integralanalytics.com',
    license='MIT',
    classifiers=classifiers,
    keywords='ETL',
    packages=find_packages(),
    install_requires=['']
)