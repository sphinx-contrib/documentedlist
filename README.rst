
DocumentedList Sphinx Extension
===============================

This file provides a Sphinx extension to convert a Python list into
a table in the generated documentation. The intended application of
this extension is to document the items of essentially list-like
objects of immutable data (possibly enums, though python 3.4 enums
are not supported yet).

In the source code, each list item, instead of being just it's native
data type, should be replaced by a tuple of two elements. The second
element of the tuple should be a string which provides a description
for the item.

In the first use of this extension, the aim is to document a list of
supported device classes (each of which is a string). This was
originally specified in the python code as a list, and the same list
with descriptions was manually maintained (or, in reality, left
unmaintained) in the corresponding documentation. The list is now
replaced with a tuple containing both the recognized strings and the
description for each, and Sphinx is able to use this extension to
'autogenerate' the table in the documentation.

Based heavily on slides from Doug Hellman's PyCon talk,
http://www.slideshare.net/doughellmann/better-documentation-through-automation-creating-docutils-sphinx-extensions

Installation & Usage
--------------------

To use this module, place the ``documentedlist.py`` file somewhere in
the ``PYTHONPATH`` that Sphinx is configured to use, or add the git
checkout folder to the ``PYTHONPATH`` in Sphinx's ``conf.py``.

In the .rst file where the table should appear, insert the Sphinx
directive provided by this module :

    .. code-block:: rest

        .. documentedlist::
            :listobject: full.importable.path.of.thelist

This extension will import the list as :

    .. code-block:: python

        from full.importable.path.of import thelist

Optionally, the headers to be displayed in the table can also be
specified. The number of columns displayed is 2 by default, and if
more columns are desired, the headers should be manually specified
with as many columns as needed, for example


foo.py :

    .. code-block:: python

        lst = [
           ["John", "Doe", "john@example.com"]
        ]

example.rst :

    .. code-block:: rest

        .. documentedlist::
            :listobject: foo.lst
            :header: "First Name" "Last Name" Email


For a usage example, see:

https://github.com/chintal/tendril/blob/public/tendril/conventions/electronics.py#L28

and the corresponding documentation generated at:

http://tendril.chintal.in/doc/userdoc/conventions/gedasymbols/#device-classes

License
-------

This Sphinx Extension is made available under the BSD 2-clause License. See
sphinxcontrib's LICENSE file for the full text.
