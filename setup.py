from setuptools import setup

import elifecrossref

with open('README.rst') as fp:
    readme = fp.read()

setup(name='elifecrossref',
    version=elifecrossref.__version__,
    description='eLife Crossref deposit of journal articles.',
    long_description=readme,
    packages=['elifecrossref'],
    license = 'MIT',
    url='https://github.com/elifesciences/elife-crossref-xml-generation',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='py@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        ]
    )
