Basic Paging Sample
===================

This sample executes a `McAfee Active Response` search for the running processes on a particular endpoint as specified
by its IP address.

The names of the processes are received in pages and displayed.

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* A McAfee Active Response (MAR) Service is available on the DXL fabric
* The Python client has been authorized to perform MAR searches (see
  `Authorize Client To Perform MAR Search <https://opendxl.github.io/opendxl-client-python/pydoc/marsendauth.html>`_
  in the OpenDXL Python SDK Documentation)

Configuration
*************

Update the following line in the sample:

    .. code-block:: python

        HOST_IP = "<SPECIFY_IP_ADDRESS>"

To specify the IP address of a host to retrieve the process list from. For Example:

    .. code-block:: python

        HOST_IP = "192.168.1.1"

Running
*******

To run this sample execute the ``sample/basic/basic_paging_example.py`` script as follows:

    .. parsed-literal::

        c:\\dxlmarclient-\ |version|\>python sample/basic/basic_paging_example.py

The output should appear similar to the following:

    .. code-block:: python

        Page: 1
            MARService.exe
            OneDrive.exe
            RuntimeBroker.exe
            SearchIndexer.exe
            SearchUI.exe
        Page: 2
            ShellExperienceHost.exe
            SkypeHost.exe
            System
            UpdaterUI.exe
            VGAuthService.exe
        Page: 3
            WUDFHost.exe
            WmiApSrv.exe
            WmiPrvSE.exe
            WmiPrvSE.exe
            [System Process]

        ...

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # The size of each page
        PAGE_SIZE = 5
        # The IP address of the host to retrieve the processes for
        HOST_IP = "192.168.1.1"

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            # Create the McAfee Active Response (MAR) client
            marclient = MarClient(client)

            # Start the search
            results_context = \
                marclient.search(
                    projections=[{
                        ProjectionConstants.NAME: "Processes",
                    }],
                    conditions={
                        ConditionConstants.OR: [{
                            ConditionConstants.AND: [{
                                ConditionConstants.COND_NAME: "HostInfo",
                                ConditionConstants.COND_OUTPUT: "ip_address",
                                ConditionConstants.COND_OP: OperatorConstants.EQUALS,
                                ConditionConstants.COND_VALUE: HOST_IP
                            }]
                        }]
                    }
                )

            # Iterate the results of the search in pages
            if results_context.has_results:
                for index in range(0, results_context.result_count, PAGE_SIZE):
                    # Retrieve the next page of results (sort by process name, ascending)
                    results = results_context.get_results(index, PAGE_SIZE,
                                                          sort_by="Processes|name",
                                                          sort_direction=SortConstants.ASC)
                    # Display items in the current page
                    print "Page: " + str((index/PAGE_SIZE)+1)
                    for item in results[ResultConstants.ITEMS]:
                        print "    " + item[ResultConstants.ITEM_OUTPUT]["Processes|name"]

Once a connection is established to the DXL fabric, a :class:`dxlmarclient.client.MarClient` instance is created
which will be used to perform searches.

Next, a search to collect process information from a particular system (as specified by its IP address)
is performed by invoking the :func:`dxlmarclient.client.MarClient.search` method of the
:class:`dxlmarclient.client.MarClient` instance.

Once the search has completed, the processes that were found on the system are displayed in pages sorted by
process name in ascending order. The :func:`dxlmarclient.client.ResultsContext.get_results` method of the
:class:`dxlmarclient.client.ResultsContext` object is invoked for each page that is displayed.

It is also worth noting that in this particular sample `constants` are used for the key names when describing
the search `projections` and `conditions`. `Constants` are also used when processing the results of the search. See the
:class:`dxlmarclient.constants` package for more information on the `constants` that are available for use with
the MAR DXL Python client.

While the use of `constants` is completely optional, it avoids hard-coding strings that could be mistyped and
is especially useful within integrated development environments (IDEs) that perform auto-completion.


