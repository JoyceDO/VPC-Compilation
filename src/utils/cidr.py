from ipaddress import *


class CIDR(IPv4Interface):
    def __init__(self, cidr):
        super().__init__(cidr)

    @property
    def a1(self):
        return self.packed[0]

    @property
    def a2(self):
        return self.packed[1]

    @property
    def a3(self):
        return self.packed[2]

    @property
    def a4(self):
        return self.packed[3]

    @property
    def prefixlen(self):
        return self.network.prefixlen


