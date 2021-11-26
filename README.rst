elife-crossref-xml-generation
=============================

Crossref deposit of journal articles

Overview
========

elife-crossref-xml-generation creates a Crossref content registration file for a journal article. The registration file is an XML file conforming to the Crossref schema. The code library is used by eLife in its publishing workflow to submit the content registration file by a POST request to the Crossref API endpoint, in order to register DOI values and metadata at Crossref. Following some basic changes to a configuration file, it should be able to generate Crossref content registration files for non-eLife journals.

This library is intended for use by developers, typically integrated into a workflow. There are some options and decisions to make for how you connect it ot your existing workflows, or create an interface to convert individual JATS XML files via a web form, for example.

Supported features
==================

* DOI
* article title and basic metadata (volume, issue, pub date, issn, etc.)
* contributors
* abstract
* Fundref
* AccessIndicators
* relations (inter_work_relation)
* text and data mining (TDM) links
* citation_list
* components (if you have component DOI values)

Ways to implement it
====================

The data passes through distinct steps, and at these steps the data can be altered if you would like to in your implementation of the library. The default data conversion begins with a JATS XML file, the XML is parsed to extract values into article objects, the article objects are used in a crossrefXML object to construct a Crossref XML representation of the data, and finally the CrossrefXML object can produce XML output. 

  JATS XML -> article objects -> CrossrefXML object -> Crossref XML output

There are situations you may want to manipulate the data prior to generating Crossref XML. For example, if the article XML is missing a publication date, or you want to specify a version of the article, then you could manipulate the objects in this way before you instantiate the CrossrefXML object.

  JATS XML -> article objects -> manipulate the objects -> CrossrefXML object -> Crossref XML output

Another way you can use this library

  JATS XML -> article objects -> manipulate the objects -> CrossrefXML object -> Crossref XML output

Install
=======

a) Install it locally

Clone the git repo

.. code-block:: bash

  git clone https://github.com/elifesciences/elife-crossref-xml-generation.git

Create a python virtual environment and activate it

.. code-block:: bash

  virtualenv venv
  source venv/bin/activate

Install it locally

.. code-block:: bash

  pip install -r requirements.txt
  pip setup.py install

b) Or, integrate it into your project

Add to your requirements.txt file of your project a particular commit of this library, for example:

.. code-block:: bash

  git+https://github.com/elifesciences/elife-crossref-xml-generation.git@288f0bc8d1148eb1795c8ae18a3985d30ba38cd5#egg=elifecrossref

Then you should be able to import the library as `elifecrossref`.

Configuration
=============

The crossref.cfg file can edited to include your particular values and options. There are some default options, and then a section for each journal to override the default values. Each particular option may support a string, boolean, integer, or list of values. Create a section of your own in the style of [journal_name] and then add the values below it you want to override.

Example usage
=============

In interactive Python, below is an example.

.. code-block:: python

    >>> from elifecrossref import generate
    >>> articles = generate.build_articles_for_crossref(["tests/test_data/elife-00666.xml"])
    >>> articles[0].version = 1
    >>> print generate.crossref_xml(articles, "elife")

There are other options in the `generate.py` file to return the CrossrefXML object created, or to write the output to disk using a single function call.

Contributing to the project
===========================

If you have a contribution you would like us to consider, please send a pull request. Open an issues on Github if you get an error. There may be minor changes required to support alternate JATS XML variations. If your XML is open licensed, we may want to add it specifically to the test cases for the project.

License
=======

`The MIT License <http://opensource.org/licenses/mit-license.php>`_
