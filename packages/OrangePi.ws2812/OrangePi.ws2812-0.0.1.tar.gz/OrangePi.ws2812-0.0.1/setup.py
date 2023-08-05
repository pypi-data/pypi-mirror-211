from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware',
               'Topic :: System :: Hardware :: Hardware Drivers']

setup(
    name		= "OrangePi.ws2812",
	version		= "0.0.1",
	description	= "Python bindings for WS2812 communication over SPI.MOSI",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
	author		= "Joost Witteveen",
	author_email	= "joosteto@gmail.com",
	maintainer	= "Joost Witteveen",
	maintainer_email= "joosteto@gmail.com",
	license		= "GPLv2",
    install_requires=[
        'spidev'
	],
	classifiers	= classifiers,
	url		= "http://github.com/joosteto/raspberry_ws2812",
	packages=find_packages()
)