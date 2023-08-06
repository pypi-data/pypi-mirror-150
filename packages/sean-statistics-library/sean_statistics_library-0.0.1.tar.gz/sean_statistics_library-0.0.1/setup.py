from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sean_statistics_library',
    version='0.0.1',
    description='Some basic statistics functions',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Sean Spitler',
    author_email='midtree5784@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Statistics',
    packages=find_packages(),
    install_requires=['']
)