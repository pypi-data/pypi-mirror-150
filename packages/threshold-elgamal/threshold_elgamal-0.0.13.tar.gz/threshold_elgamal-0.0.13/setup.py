from setuptools import setup
from codecs import open

setup(
    name='threshold_elgamal',
    version='0.0.13',
    long_description_content_type="text/markdown",
    long_description=open('README.md', 'r').read(),
    packages=['tests', 'threshold_elgamal'],
    url='https://threshold-elgamal.readthedocs.io/en/latest/index.html',
    download_url='https://gitlab.com/kboras/threshold-elgamal',
    license='',
    author='Katarina Boras',
    author_email='katarina.boras2@outlook.com',
    description='Threshold ElGamal cryptosystem'
)
