Basic Search Sample
===================

This sample executes a `McAfee Active Response` search for the IP addresses of hosts that have an Active Response client
installed.

This is the same sample that is available in the OpenDXL Python SDK
(see `McAfee Active Response Search Sample <https://opendxl.github.io/opendxl-client-python/pydoc/marsearchexample.html>`_),
but has been refactored to use the McAfee Active Response (MAR) DXL client library.

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* A McAfee Active Response (MAR) Service is available on the DXL fabric
* The Python client has been authorized to perform MAR searches (see
  `Authorize Client To Perform MAR Search <https://opendxl.github.io/opendxl-client-python/pydoc/marsendauth.html>`_
  in the OpenDXL Python SDK Documentation)

Running
*******

To run this sample execute the ``sample/basic/basic_search_example.py`` script as follows:

    .. parsed-literal::

        c:\\dxlmarclient-python-sdk-\ |version|\>python sample/basic/basic_search_example.py

The output should appear similar to the following:

    .. code-block:: python

        Results:
            192.168.130.152
            192.168.130.133

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            # Create the McAfee Active Response (MAR) client
            mar_client = MarClient(client)

            # Performs the search
            result_context = \
                mar_client.search(
                    projections=[{
                        "name": "HostInfo",
                        "outputs": ["ip_address"]
                    }]
                )

            # Loop and display the results
            if result_context.has_results:
                search_result = result_context.get_results(limit=10)
                print "Results:"
                for item in search_result["items"]:
                    print "    " + item["output"]['HostInfo|ip_address']


Once a connection is established to the DXL fabric, a :class:`dxlmarclient.client.MarClient` instance is created
which will be used to perform searches.

Next, a search to collect the IP addresses for monitored systems is performed by invoking
the :func:`dxlmarclient.client.MarClient.search` method of the :class:`dxlmarclient.client.MarClient` instance.

Once the search has completed, the first 10 results are retrieved by invoking the
:func:`dxlmarclient.client.ResultsContext.get_results` method of the :class:`dxlmarclient.client.ResultsContext`
object that was returned from invoking the search method. The results are iterated and printed to the screen.


