from setuptools import setup, find_packages

setup(
    name='adaptiveheatmap',
    version="0.0.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Takafumi Arakaki',
    author_email='aka.tkf@gmail.com',
    # url='https://github.com/tkf/adaptiveheatmap',
    license='BSD-2-Clause',  # SPDX short identifier
    # description='adaptiveheatmap - THIS DOES WHAT',
    long_description=open('README.rst').read(),
    # keywords='KEYWORD, KEYWORD, KEYWORD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        # 'SOME_PACKAGE',
    ],
    # entry_points={
    #     'console_scripts': ['PROGRAM_NAME = adaptiveheatmap.cli:main'],
    # },
)
