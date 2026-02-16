class PrefixListCidr:
    def __init__(
        self,
        cidr: str,
        description: str,
    ):
        self.CIDR = cidr
        self.DESCRIPTION = description

    def validate_cidr(self):
        if "/16" in self.CIDR:
            raise ValueError("CIDR must not be /16")
