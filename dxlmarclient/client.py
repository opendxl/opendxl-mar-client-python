# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2016 McAfee Inc. - All Rights Reserved.
################################################################################

import json
import logging
import time
from dxlclient import Request, Message
from constants import SortConstants

# Configure local logger
logger = logging.getLogger(__name__)

# The McAfee Active Response (MAR) search topic
MAR_SEARCH_TOPIC = "/mcafee/mar/service/api/search"


class MarClient(object):
    """
    This client provides a high level wrapper for communicating with the McAfee Active Response (MAR) DXL service.

    The purpose of this client is to allow the user to perform MAR searches without having to focus on
    lower-level details such as MAR-specific DXL topics and message formats.
    """

    # The default amount of time (in seconds) to wait before polling the MAR server for results
    __DEFAULT_POLL_INTERVAL = 5
    # The minimum amount of time (in seconds) to wait before polling the MAR server for results
    __MIN_POLL_INTERVAL = 5
    # The default amount of time (in seconds) to wait for a response from the MAR server
    __DEFAULT_RESPONSE_TIMEOUT = 30
    # The minimum amount of time (in seconds) to wait for a response from the MAR server
    __MIN_RESPONSE_TIMEOUT = 30

    def __init__(self, dxl_client):
        """
        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the MAR DXL service
        """
        self.__dxl_client = dxl_client
        self.__poll_interval = self.__DEFAULT_POLL_INTERVAL
        self.__response_timeout = self.__DEFAULT_RESPONSE_TIMEOUT

    @property
    def poll_interval(self):
        """
        The amount of time to wait (in seconds) before polling the MAR server for results
        """
        return self.__poll_interval

    @poll_interval.setter
    def poll_interval(self, poll_interval):
        if poll_interval < self.__MIN_POLL_INTERVAL:
            raise Exception("Poll interval must be greater than or equal to " + str(self.__MIN_POLL_INTERVAL))
        self.__poll_interval = poll_interval

    @property
    def response_timeout(self):
        """
        The maximum amount of time (in seconds) to wait for a response from the MAR server
        """
        return self.__response_timeout

    @response_timeout.setter
    def response_timeout(self, response_timeout):
        if response_timeout < self.__MIN_RESPONSE_TIMEOUT:
            raise Exception("Response timeout must be greater than or equal to " + str(self.__MIN_RESPONSE_TIMEOUT))
        self.__response_timeout = response_timeout

    def search(self, projections, conditions=None):
        """
        Executes a search via McAfee Active Response.

        Once the search has completed a :class:`ResultsContext` object is returned which is used to access the
        search results.

        .. note::

            **Client Authorization**

            The OpenDXL Python client invoking this method must have permission to send messages to the
            ``/mcafee/mar/service/api/search`` topic.

            See the following page for details on authorizing a client to perform MAR searches:

            `<https://opendxl.github.io/opendxl-client-python/pydoc/marsendauth.html>`_

        Execution of a MAR search requires a ``list`` of `projections` and an optional ``dictionary`` containing
        the search `conditions`.

        **Projections**

            `Projections` are used to describe the information to collect in the search. Each `projection` consists
            of a `collector` name and a list of `output names` from the `collector`. For example, the
            ``Processes`` `collector` includes `output names` such as ``name``, ``sha1``, ``md5``, etc.

            For a complete list of `collectors` and their associated `output names` refer to the
            `McAfee Active Response Product Guide`.

            Each `projection` specified must contain the following fields:

            * ``name``: The name of the `collector` to project
            * ``outputs``: An array of `output names` of the `collector` to project

            The python ``list`` below is equivalent to the `projections` within the following textual search:

            ``Processes name, id where Processes name equals "csrss" and Processes name contains "exe" or Processes
            size not greater than 200``

            .. code-block:: python

                projections=[{
                    "name": "Processes",
                    "outputs": ["name", "id"]
                }]

        **Conditions**

            `Conditions` are used to restrict which items are included in the search results. For example, a search
            that collects process-related information could be limited to those processes which match a specified name.

            A condition has a fixed structure starting with an ``or`` conditional operator and allowing only one level
            of ``and`` conditions.

            The python ``dictionary`` below is equivalent to the `conditions` within the following textual search:

            ``Processes name, id where Processes name equals "csrss" and Processes name contains "exe" or Processes
            size not greater than 200``

            .. code-block:: python

                conditions={
                    "or": [{
                        "and": [{
                            "name": "Processes",
                            "output": "name",
                            "op": "EQUALS",
                            "value": "csrss"
                        }, {
                            "name": "Processes",
                            "output": "name",
                            "op": "CONTAINS",
                            "value": "exe"
                        }]
                    }, {
                        "and": [{
                            "name": "Processes",
                            "output": "size",
                            "op": "GREATER_THAN",
                            "value": "200",
                            "negated": "true"
                        }]
                    }]
                }

            The following fields are used for each `condition`:

            * ``name``: The name of the `collector` from which to retrieve a value for comparison
            * ``output``: The `output name` from the `collector` that selects the specific value to use for comparison
            * ``op``: The comparison operator
            * ``value``: The value to compare with the value from the `collector`
            * ``negated``: (optional) Indicates if the comparison is negated

            The operators available for each value data type are as follows:

                +--------------------+--------+--------+---------+------+----------+--------------+
                | Operator           | NUMBER | STRING | BOOLEAN | DATE | IPV4IPV6 | REG_STR      |
                +====================+========+========+=========+======+==========+==============+
                | GREATER_EQUAL_THAN |    x   |        |         |      |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | GREATER_THAN       |    x   |        |         |      |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | LESS_EQUAL_THAN    |    x   |        |         |      |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | LESS_THAN          |    x   |        |         |      |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | EQUALS             |    x   |   x    |    x    |   x  |     x    |  x ``(*)``   |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | CONTAINS           |        |   x    |         |      |     x    |  x ``(*)``   |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | STARTS_WITH        |        |   x    |         |      |          |  x ``(*)``   |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | ENDS_WITH          |        |   x    |         |      |          |  x ``(*)``   |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | BEFORE             |        |        |         |   x  |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                | AFTER              |        |        |         |   x  |          |              |
                +--------------------+--------+--------+---------+------+----------+--------------+
                ``(*)`` Negated field is not supported in those cases.

            **Example Usage**

                .. code-block:: python

                    # Create the client
                    with DxlClient(config) as client:

                        # Connect to the fabric
                        client.connect()

                        # Create the McAfee Active Response (MAR) client
                        marclient = MarClient(client)

                        # Execute the search
                        results_context = marclient.search(
                                projections=[{
                                    "name": "Processes",
                                    "outputs": ["name", "id"]
                                }],
                                conditions={
                                    "or": [{
                                        "and": [{
                                            "name": "Processes",
                                            "output": "name",
                                            "op": "EQUALS",
                                            "value": "csrss"
                                        }, {
                                            "name": "Processes",
                                            "output": "name",
                                            "op": "CONTAINS",
                                            "value": "exe"
                                        }]
                                    }, {
                                        "and": [{
                                            "name": "Processes",
                                            "output": "size",
                                            "op": "GREATER_THAN",
                                            "value": "200",
                                            "negated": "true"
                                        }]
                                    }]
                                }
                            )

        :param projections: A ``list`` containing the `projections` for the search
        :param conditions: (optional) A ``dictionary`` containing the `conditions` for the search
        :return: A :class:`ResultsContext` object which is used to access the search results.
        """
        request_dict = {
            "target": "/v1/simple",
            "method": "POST",
            "parameters": {},
            "body": {
                "projections": projections
            }
        }

        if conditions:
            request_dict["body"]["condition"] = conditions

        # Create the search
        response_dict = self._invoke_mar_search_api(request_dict)

        # Get the search identifier
        search_id = response_dict["body"]["id"]

        # Start the search
        self._invoke_mar_search_api({
            "target": "/v1/" + search_id + "/start",
            "method": "PUT",
            "parameters": {},
            "body": {}
        })

        # Wait until the search finishes
        finished = False
        body = None
        while not finished:
            response_dict = self._invoke_mar_search_api({
                "target": "/v1/" + search_id + "/status",
                "method": "GET",
                "parameters": {},
                "body": {}
            })
            body = response_dict["body"]
            finished = body["status"] == "FINISHED"
            if not finished:
                time.sleep(self.__poll_interval)

        # Return the results information
        return ResultsContext(self, search_id,
                              body["results"], body["errors"], body["hosts"], body["subscribedHosts"])

    def _invoke_mar_search_api(self, payload_dict):
        """
        Executes a query against the MAR search API

        :param payload_dict: The payload
        :return: A dictionary containing the results of the query
        """
        # Create the request message
        req = Request(MAR_SEARCH_TOPIC)
        # Set the payload
        req.payload = json.dumps(payload_dict).encode(encoding="UTF-8")

        # Display the request that is going to be sent
        logger.debug("Request:\n" + json.dumps(payload_dict, sort_keys=True, indent=4, separators=(',', ': ')))

        # Send the request and wait for a response (synchronous)
        res = self.__dxl_client.sync_request(req, timeout=self.__response_timeout)

        # Return a dictionary corresponding to the response payload
        if res.message_type != Message.MESSAGE_TYPE_ERROR:
            resp_dict = json.loads(res.payload.decode(encoding="UTF-8"))
            # Display the response
            logger.debug("Response:\n" + json.dumps(resp_dict, sort_keys=True, indent=4, separators=(',', ': ')))
            if "code" in resp_dict:
                code = resp_dict['code']
                if code < 200 or code >= 300:
                    if "body" in resp_dict and "applicationErrorList" in resp_dict["body"]:
                        error = resp_dict["body"]["applicationErrorList"][0]
                        raise Exception(error["message"] + ": " + str(error["code"]))
                    elif "body" in resp_dict:
                        raise Exception(resp_dict["body"] + ": " + str(code))
                    else:
                        raise Exception("Error: Received failure response code: " + str(code))
            else:
                raise Exception("Error: unable to find response code")
            return resp_dict
        else:
            raise Exception("Error: " + res.error_message + " (" + str(res.error_code) + ")")


class ResultsContext(object):
    """
    This object is used to access to the results of a MAR search (see :func:`MarClient.search`).
    """
    def __init__(self, mar_client, search_id, result_count, error_count, host_count, subscribed_host_count):
        self.__mar_client = mar_client
        self.__search_id = search_id
        self.__result_count = result_count
        self.__error_count = error_count
        self.__host_count = host_count
        self.__subscribed_host_count = subscribed_host_count

    @property
    def has_results(self):
        """
        Whether the search has results
        """
        return self.__result_count > 0

    @property
    def result_count(self):
        """
        The total count of items available in the search results
        """
        return self.__result_count

    @property
    def error_count(self):
        """
        The count of errors that were reported during the search
        """
        return self.__error_count

    @property
    def host_count(self):
        """
        The count of endpoints that responded to the search
        """
        return self.__host_count

    @property
    def subscribed_host_count(self):
        """
        The count of endpoints that were connected to the DXL fabric when the search started
        """
        return self.__subscribed_host_count

    def get_results(self, offset=0, limit=20, text_filter="", sort_by="count", sort_direction=SortConstants.DESC):
        """
        This method is used to retrieve a particular set of results from a MAR search.

        **Results**

            Each search result item has the following fields:

            * ``id``: The identifier of the item within the search results
            * ``count``: The number of times that the search result was reported
            * ``created_at``: The item timestamp
            * ``output``: The search result data where each key is composed of ``<CollectorName>|<OutputName>`` and
              the value that correspond to that `collector` and `output name`.

            The python ``dictionary`` below is an example of a result that would be returned from the
            following textual search:

            ``Processes name, id where Processes name equals "csrss" and Processes name contains "exe" or Processes
            size not greater than 200``

            .. code-block:: python

                {
                    "startIndex": 0,
                    "totalItems": 2,
                    "currentItemCount": 2,
                    "itemsPerPage": 20,
                    "items": [
                        {
                            "id": "{1=[[System Process], 0]}",
                            "count": 2,
                            "created_at": "2016-11-16T22:50:04.650Z",
                            "output": {
                                "Processes|id": 0,
                                "Processes|name": "[System Process]"
                            }
                        },
                        {
                            "id": "{1=[System, 4]}",
                            "count": 1,
                            "created_at": "2016-11-16T22:50:04.650Z",
                            "output": {
                                "Processes|id": 4,
                                "Processes|name": "System"
                            }
                        }
                    ]
                }

        **Example Usage**

            .. code-block:: python

                results = results_context.get_results(sort_by="Processes|name", sort_direction="asc")

                # Display items
                for item in results["items"]:
                    print "    " + item["output"]["Processes|name"]

        :param offset: (optional) Index of the first result item to be returned. This value is ``0`` based.
            Default value: ``0``
        :param limit: (optional) The maximum number of items to return in the results. Default value: ``20``
        :param text_filter: (optional) A text based filter to limit the results (this can be any string)
        :param sort_by: (optional) The field that will be used to sort the results. Default value: ``count``
        :param sort_direction: (optional) values: ascending ``asc`` or descending ``desc`` (String).
            Default value: ``desc``
        :return: A ``dictionary`` containing the specified results from the search.
        """

        # Get the search results
        search_result =\
            self.__mar_client._invoke_mar_search_api({
                "target": "/v1/" + self.__search_id + "/results",
                "method": "GET",
                "parameters": {
                    "$offset": offset,
                    "$limit": limit,
                    "filter": text_filter,
                    "sortBy": sort_by,
                    "sortDirection": sort_direction
                },
                "body": {}
            })

        if "body" in search_result:
            return search_result["body"]
        else:
            raise Exception("Unable to find 'body' in search result.")
