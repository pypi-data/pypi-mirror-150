from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Module for Speech Processing'
AUTHOR = 'Ittipon Bangudsareh'
EMAIL = 'edocstudio.info@gmail.com'

# Setting up
setup(
    name="pyspeechanalysis",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'speech', 'signal', 'processing', 'speech processing', 'signal processing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
)