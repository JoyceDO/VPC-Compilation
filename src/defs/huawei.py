import uuid
from utils.cidr import CIDR


class HW_Object(object):
    def __init__(self, name=''):
        self.id = uuid.uuid4()  # uuid形式的资源标识符
        self.name = name
        self.description = ''


class HW_ESC(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cidr = None
        self.availability_zone = ''  # 可用区
        self.vpc_id = ''
        self.vpc_sn_id=''
        self.sg_id=''
        self.eip=''


class HW_EIP(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cidr = None
        self.type = ''  #[ 'dynamic BGP', 'static BGP']
        self.bandwidth=1



class HW_ELB(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cidr = None
        self.vpc_id = ''
        self.vpc_sn_id = ''
        self.type = ''  # [ 'public network', 'private network']
        self.eip = ''  # only for public network ELB
        self.monitors = []


    def __str__(self):
        return '<type: {}>' \
                .format(self.type)


class HW_Monitor(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.front_end_protocol = ''  # ['TCP','UDP','HTTP','HTTPS']
        self.front_end_port = 0
        self.server_groups = []

    def __str__(self):
        return '<front end protocol: {}, front end port: {}>' \
                .format(self.front_end_protocol, self.front_end_port)


class HW_Server_Group(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_end_protocol = ''  # same as the front end protocol in corresponding Monitor
        self.distri_strategy = ''  # ['WRR', 'Weighted Least Connections', 'Source IP Algorithm']
        self.esc_list = []

    def __str__(self):
        return '<back end protocol: {}, distribution strategy: {}>' \
                .format(self.back_end_protocol, self.distri_strategy)


MONITOR_PROTOCOLS = ('TCP', 'UDP', 'HTTP', 'HTTPS')
DISTRIBUTION_STRATEGY = ('WRR', 'Weighted Least Connections', 'Source IP Algorithm')


def add_monitor(elb, protocol, port):
    assert protocol in MONITOR_PROTOCOLS

    monitor = HW_Monitor()
    monitor.front_end_protocol = protocol
    monitor.front_end_port = port
    elb.monitors.append(monitor)
    return monitor


def add_server_group(monitor, dis_strategy):
    assert dis_strategy in DISTRIBUTION_STRATEGY

    server_group = HW_Server_Group()
    server_group.back_end_protocol = monitor.front_end_protocol
    server_group.distri_strategy = dis_strategy
    monitor.server_groups.append(server_group)
    return server_group


class HW_VPC(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cidr = None  # VPC下可用子网的范围, 形如 ip/mask, eg: 192.168.0.0/16
        self.subnets = []  # ids of subnets
        self.subnet_prefixlen = 24
        self.next_subnet_index = 0

    def next_subnet_cidr(self):
        sn_list = list(self.cidr.network.subnets(new_prefix=self.subnet_prefixlen))
        index = self.next_subnet_index
        self.next_subnet_index += 1
        if index < len(sn_list):
            return CIDR(sn_list[index])
        else:
            return None


class HW_Subnet(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cidr = None  # 必须在 VPC 的网段范围内
        self.availability_zone = ''  # 可用区
        self.route_table = None
        self.vpc_id = ''
        self.hosts = []  # ids of hosts
        self.acls = []  # ids of access control lists
        self.elbs= []
        self.int_router_id = None  # internal use
        self.int_subnet_id = None  # internal use


class HW_Host(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subnet_id = ''
        self.ip = ''
        self.eip = ''  # optional
        self.availability_zone = ''
        self.security_groups = []  # ids of security groups


class HW_Peering(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vpc1_id = ''
        self.vpc2_id = ''


class HW_Security_Group(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.security_group_rules = []  # objects


class HW_SG_Rule(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.security_group_id = ''
        self.direction = ''  # ['egress', 'ingress']
        self.ethertype = ''  # ['IPv4', SG_ID]

        # ethertype == 'IPv4'
        self.protocol = ''  # ['ICMP', 'TCP', 'UDP', 'GRE', 'ALL']
        self.src_ip = ''  # eg: 192.168.0.0/24
        self.port = 0

        # ethertype == SG_ID
        self.remote_group_id = ''  # just like src_ip in 'IPV4'


ACL_ACTIONS = ('allow', 'deny')
ACL_PROTOCOLS = ('TCP', 'UDP', 'ICMP', 'ALL')


class HW_ACL(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acl_rules = []  # objects

        # add default rule
        default_rule = HW_ACL_Rule()
        default_rule.enabled = True
        self.acl_rules.append(default_rule)


class HW_ACL_Rule(HW_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = 'allow'  # ['allow', 'deny']
        self.enabled = False
        self.protocol = 'ALL'  # ['TCP', 'UDP', 'ICMP', 'ALL']
        self.src_ip_addr = CIDR('0.0.0.0/0')
        self.src_port = (0, 0)  # 端口范围, eg: (21, 23), 左开右闭, 即: [21, 23), 包含 21, 22
        self.dst_ip_addr = CIDR('0.0.0.0/0')
        self.dst_port = (0, 0)
        self.priority = -1  # 1为最大，数字越大优先级越低，此值取决于规则建立顺序，用户无法修改

    def __str__(self):
        return '<priority: {}, action: {}, protocol: {}, src ip: {}, dst ip: {}, src port: {}, dst port: {}>' \
               .format(self.priority, self.action, self.protocol,
                       self.src_ip_addr, self.dst_ip_addr, self.src_port, self.dst_port)


def add_acl_rule(acl, action, protocol, src_ip, dst_ip, src_port=(0, 0), dst_port=(0, 0)):
    assert action in ACL_ACTIONS
    assert protocol in ACL_PROTOCOLS
    assert isinstance(src_ip, CIDR)
    assert isinstance(dst_ip, CIDR)

    rule = HW_ACL_Rule()
    rule.action = action
    rule.enabled = True
    rule.protocol = protocol
    rule.src_ip_addr = src_ip
    rule.dst_ip_addr = dst_ip
    rule.src_port = src_port
    rule.dst_port = dst_port
    rule.priority = len(acl.acl_rules)
    acl.acl_rules.insert(len(acl.acl_rules)-1, rule)
    return rule

# End of file
