from setuptools import setup

import elifecrossref

with open("README.rst") as fp:
    README = fp.read()

setup(
    name="elifecrossref",
    version=elifecrossref.__version__,
    description="eLife Crossref deposit of journal articles.",
    long_description=README,
    long_description_content_type="text/x-rst",
    packages=["elifecrossref"],
    license="MIT",
    install_requires=[
        "elifetools",
        "elifearticle",
        "GitPython",
        "configparser",
        "requests",
    ],
    url="https://github.com/elifesciences/elife-crossref-xml-generation",
    maintainer="eLife Sciences Publications Ltd.",
    maintainer_email="py@elifesciences.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
