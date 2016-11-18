# This sample executes a McAfee Active Response search for the IP addresses
# of hosts that have an Active Response client installed.

import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlmarclient import MarClient

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

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
