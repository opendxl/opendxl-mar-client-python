Library Installation
====================

Prerequisites
*************

* OpenDXL Python Client library installed
 * `<https://github.com/opendxl/opendxl-client-python>`_
* The OpenDXL Python Client prerequisites must be satisfied
 * `<https://opendxl.github.io/opendxl-client-python/pydoc/installation.html>`_
* McAfee Active Response Server installed and available on DXL fabric
 * `<http://www.mcafee.com/us/products/endpoint-threat-defense-response.aspx>`_

Installation
************

Use ``pip`` to automatically install the module:

    .. parsed-literal::

        pip install dxlmarclient-\ |version|\-py2.7-none-any.whl

Or with:

    .. parsed-literal::

        pip install dxlmarclient-\ |version|\.zip

As an alternative (without PIP), unpack the dxlmarclient-\ |version|\.zip (located in the lib folder) and run the setup
script:

    .. parsed-literal::

        python setup.py install


