from typing import TypedDict
from ipaddress import IPv4Address


class VDS_Rule(TypedDict):
    description: str
    action: str
    protocol: str
    source_address: IPv4Address
    source_port: str
    destination_address: IPv4Address
    destination_address: str
    comment: str
