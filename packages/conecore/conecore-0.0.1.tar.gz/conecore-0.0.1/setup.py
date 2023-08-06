from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
]

setup(
    name='conecore',
    version='0.0.1',
    description='It is a code which is completely looks like tkinter but with little differences',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ahmed Baligh',
    author_email='ahmedgamejd1992@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Tkinter',
    packages=find_packages(),
    install_requires=['']
)