# This sample executes a McAfee Active Response search for a Hash
# of hosts with specific maGuids.

from __future__ import absolute_import
from __future__ import print_function

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

with DxlClient(config) as client:

    client.connect()
    marclient = MarClient(client)

    results_context = marclient.search(
        projections=[{
            "name": "HostInfo",
            "outputs": ["hostname", "ip_address"]
        }, {
            "name": "Files",
            "outputs": ["md5", "status"]
        }],
        conditions={
            "or": [{
                "and": [{
                "name": "Files",
                "output": "md5",
                "op": "EQUALS",
                "value": "daac6ba6967893ddea06ed132b781529"
                }]
            }]
        },
        context={
            "maGuids": [
                "{A53CB87C-37F4-11E8-3671-00000007327C}".lower()
            ]
        }
    )

    # Loop and display the results
    if result_context.has_results:
        search_result = result_context.get_results(limit=10)
        print("Results:")
        for item in search_result["items"]:
            print("    " + item["output"]['HostInfo|ip_address'])
