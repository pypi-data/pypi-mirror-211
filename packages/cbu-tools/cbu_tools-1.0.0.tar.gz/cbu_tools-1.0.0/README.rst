cbu_tools
=======================

:code:`cbu_tools` is a Python package that provides tools for working with Clave Bancaria Uniforme (CBU) numbers, which are bank account identifiers used in Argentina.

Features
---------
- Validate a CBU number

Installation
------------
You can install :code:`cbu_tools` using :code:`pip`:

.. code-block:: bash

    $ pip install cbu_tools

Usage
-----
Once installed, you can import the :code:`CBU` class from :code:`cbu_tools` and use it to validate CBU numbers:

.. code-block:: python

    from cbu_tools import CBU

    cbu = CBU("0170099220000067797370")

    if cbu.is_valid():
        print("Valid CBU")
    else:
        print("Invalid CBU")

Please note that :code:`is_valid` merely validates the format and checksum of a CBU according to the `algorithm specified for CBU validation <https://es.wikipedia.org/wiki/Clave_Bancaria_Uniforme>`_. It does not perform any verification or validation against external systems to determine if the CBU exists or if it is associated with a specific person or entity.

Running Tests
-------------
You can run the tests using :code:`tox`:

.. code-block:: bash

    $ tox

License
-------
This project is licensed under the MIT License. See the LICENSE.txt file for details.