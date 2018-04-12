# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee LLC - All Rights Reserved.
################################################################################


class SortConstants(object):
    """
    Constants that describe the direction the search results should be sorted
    (ascending vs. descending)

        The following statement:

            .. code-block:: python

                results = results_context.get_results(sort_by="Processes|name",
                    sort_direction="asc")

        Can be rewritten to use :class:`SortConstants` as follows:

            .. code-block:: python

                results = results_context.get_results(sort_by="Processes|name",
                    sort_direction=SortConstants.ASC)
    """
    ASC = "asc"
    DESC = "desc"


class OperatorConstants(object):
    """
    Constants that describe the `operator` to use within a `condition`.

        The following statement:

            .. code-block:: python

                conditions={
                    "or": [{
                        "and": [{
                            "name": "HostInfo",
                            "output": "ip_address",
                            "op": "EQUALS",
                            "value": "192.168.1.1"
                        }]
                    }]
                }

        Can be rewritten to use :class:`OperatorConstants` as follows:

            .. code-block:: python

                conditions={
                    "or": [{
                        "and": [{
                            "name": "HostInfo",
                            "output": "ip_address",
                            "op": OperatorConstants.EQUALS,
                            "value": "192.168.1.1"
                        }]
                    }]
               }
    """
    GREATER_EQUAL_THAN = "GREATER_EQUAL_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL_THAN = "LESS_EQUAL_THAN"
    LESS_THAN = "LESS_THAN"
    EQUALS = "EQUALS"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    BEFORE = "BEFORE"
    AFTER = "AFTER"


class ProjectionConstants(object):
    """
    Constants that are used to describe a `projection`.

        The following statement:

            .. code-block:: python

                projections=[{
                    "name": "HostInfo",
                    "outputs": ["ip_address"]
                }]

        Can be rewritten to use :class:`ProjectionConstants` as follows:

            .. code-block:: python

                projections=[{
                    ProjectionConstants.NAME: "HostInfo",
                    ProjectionConstants.OUTPUTS: ["ip_address"]
                }]
    """

    NAME = "name"
    OUTPUTS = "outputs"


class ConditionConstants(object):
    """
    Constants that are used to describe a `condition`.

        The following statement:

            .. code-block:: python

                conditions={
                    "or": [{
                        "and": [{
                            "name": "HostInfo",
                            "output": "ip_address",
                            "op": "EQUALS",
                            "value": "192.168.1.1"
                        }]
                    }]
                }

        Can be rewritten to use :class:`ConditionConstants` as follows:

            .. code-block:: python

                conditions={
                    ConditionConstants.OR: [{
                        ConditionConstants.AND: [{
                            ConditionConstants.COND_NAME: "HostInfo",
                            ConditionConstants.COND_OUTPUT: "ip_address",
                            ConditionConstants.COND_OP: "EQUALS",
                            ConditionConstants.COND_VALUE: "192.168.1.1"
                        }]
                    }]
                }
    """
    AND = "and"
    OR = "or"
    COND_NAME = "name"
    COND_OUTPUT = "output"
    COND_OP = "op"
    COND_VALUE = "value"


class ResultConstants(object):
    """
    Constants that are used access the information contained in the results of a
    search.

        The following statement:

            .. code-block:: python

                search_result = result_context.get_results(limit=10)
                print "Total items: " + str(search_result["totalItems"])
                for item in search_result["items"]:
                    print "    " + item["output"]['HostInfo|ip_address']

        Can be rewritten to use :class:`ResultConstants` as follows:

            .. code-block:: python

                    search_result = result_context.get_results(limit=10)
                    print "Total items: " + str(search_result[ResultConstants.TOTAL_ITEMS])
                    for item in search_result[ResultConstants.ITEMS]:
                        print "    " + item[ResultConstants.ITEM_OUTPUT]['HostInfo|ip_address']
    """
    CURRENT_ITEM_COUNT = "currentItemCount"
    TOTAL_ITEMS = "totalItems"
    START_INDEX = "startIndex"
    ITEMS_PER_PAGE = "itemsPerPage"
    ITEMS = "items"
    ITEM_COUNT = "count"
    ITEM_CREATED_AT = "created_at"
    ITEM_ID = "id"
    ITEM_OUTPUT = "output"
