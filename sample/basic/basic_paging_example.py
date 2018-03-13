# This sample executes a McAfee Active Response search for the running
# processes on a particular endpoint as specified by its IP address.
#
# The names of the processes are received in pages and displayed.
#
# NOTE: Prior to running this sample you must specify an IP address for the
#       system to collect process information from in the HOST_IP constant
#       below.

from __future__ import absolute_import
from __future__ import print_function
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlmarclient import MarClient, ResultConstants, ProjectionConstants, \
    ConditionConstants, SortConstants, OperatorConstants

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# The size of each page
PAGE_SIZE = 5
# The IP address of the host to retrieve the processes for
HOST_IP = "<SPECIFY_IP_ADDRESS>"


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
            print("Page: " + str((index/PAGE_SIZE)+1))
            for item in results[ResultConstants.ITEMS]:
                print("    " + item[ResultConstants.ITEM_OUTPUT]["Processes|name"])
