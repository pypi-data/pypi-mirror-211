import json

from decouple import config

with open("./main/superfluid/src/abis/cfa_v1.json") as cfa_v1:
    cfa_v1_abi = cfa_v1.read()

CFA_V1_ABI = json.loads(cfa_v1_abi)

with open("./main/superfluid/src/abis/cfa_v1_forwarder.json") as cfa_v1_forwarder:
    cfa_v1_forwarder_abi = cfa_v1_forwarder.read()

CFA_V1_FORWARDER_ABI = json.loads(cfa_v1_forwarder_abi)

with open("./main/superfluid/src/abis/host.json") as host:
    host_abi = host.read()

HOST_ABI = json.loads(host_abi)

with open("./main/superfluid/src/metadata/networks.json") as networks:
    networks = networks.read()

NETWORKS = json.loads(networks)

RPC_FOR_MUMBAI = config("RPC_FOR_MUMBAI")

PRIVATE_KEY = config("PRIVATE_KEY")

"""
------- ACL AUTHORIZATION BIT OPERATIONS -------
"""
AUTHORIZE_FLOW_OPERATOR_CREATE = 1 << 0
AUTHORIZE_FLOW_OPERATOR_UPDATE = 1 << 1
AUTHORIZE_FLOW_OPERATOR_DELETE = 1 << 2
