from setuptools import setup 
import os
import codecs

VERSION = '0.0.2'
DESCRIPTION = 'Enables you to get typewriter animation.'
LONG_DESCRIPTION = 'This python moudle use fundamental libraries of python which help you to print your statements in a more authentic way.'

setup(
	name='slow_text',
	version = VERSION,
	author = 'Roshan Laharwani',
	description = DESCRIPTION,
	long_description_content_type = "text/markdown",
	long_description = LONG_DESCRIPTION,
	keywords = ['typewriter','python','text effect','slow text'],
	classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)