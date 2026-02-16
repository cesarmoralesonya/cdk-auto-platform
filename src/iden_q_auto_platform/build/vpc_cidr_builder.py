from cdk_auto_platform.models.vpc.ip_ranges_types import IpPrivateRanges


class VpcCidrBuilder:
    @staticmethod
    def build(ip_private_range: IpPrivateRanges) -> str:
        vpc_cidr: str = ""
        if ip_private_range == IpPrivateRanges.LARGE_COMPANY:
            vpc_cidr = ip_private_range.value + ".2.0.0/16"
        elif ip_private_range == IpPrivateRanges.BIG_COMPANY:
            vpc_cidr = ip_private_range.value + ".32.0/20"
        elif ip_private_range == IpPrivateRanges.SMALL_COMPANY:
            vpc_cidr = ip_private_range.value + ".32.0/24"

        return vpc_cidr
