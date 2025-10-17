from enum import Enum


class IpPrivateRanges(Enum):
    """
    Range of private IP addresses defined by RFC 1918
        • 10.0.0.0/16 - 65536 IP addresses
        • 172.16.0.0/20 - 4096 IP addresses
        • 192.168.0.0/24 - 256 IP addresses
    """

    LARGE_COMPANY = "10"
    BIG_COMPANY = "172.16"
    SMALL_COMPANY = "192.168"
