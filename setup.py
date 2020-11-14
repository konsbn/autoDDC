from setuptools import setup

setup(
    name='autoDDC',
    version='0.1',
    description='An ISBN based Dewey Decimal Classifier',
    url='https://github.com/konsbn/autoDDC',
    author='Shubham Bhushan',
    author_email='shubphotons@gmail.com',
    license='GPL v3',
    packages=['autoDDC'],
    install_requires=['mechanicalsoup',
                      'isbntools',
                      ],
    classifiers=[
        'Intended Audience :: Book Collectors/Libraries',
        'Programming Language :: Python :: 3',
    ],
)
