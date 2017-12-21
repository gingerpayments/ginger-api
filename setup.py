from setuptools import setup
from setuptools import find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='ginger-python',
    description='Ginger Payments API Wrapper',
    long_description=read('README.mdown'),
    version='0.1',
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords=['ginger', 'api', 'library'],
    author='Ginger Payments B.V.',
    url='https://github.com/gingerpayments/ginger-python.git',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests>=2.4.1',
        'isodate>=0.5.1',
    ],
)
