from defs.huawei import *
from algorithms.intent_network import *
from utils.cidr import *


class VPCNetwork(object):
    def trans_intent_network(self, int_nw):

        # 计算意图网的每个子网的所有可达子网, key: 子网id, value: [子网id, ]
        int_sn_conns = {}
        # 计算完全独立（无可达性）的子网
        no_conns_sn = list(int_nw.subnets)
        for ir in int_nw.intents_r.values():
            i_sid1 = ir.subnet1_id
            i_sid2 = ir.subnet2_id

            if i_sid1 not in int_sn_conns:
                int_sn_conns[i_sid1] = []
                no_conns_sn.remove(i_sid1)
            int_sn_conns[i_sid1].append(i_sid2)

            if i_sid2 not in int_sn_conns:
                int_sn_conns[i_sid2] = []
                no_conns_sn.remove(i_sid2)
            int_sn_conns[i_sid2].append(i_sid1)

        # DFS求意图网的连通分量
        visited = []
        stack = []

        # 连通分量的列表
        ccs_sn_ids = []

        for int_sn_id in int_sn_conns:
            if int_sn_id not in visited:
                visited.append(int_sn_id)
                stack.append(int_sn_id)

                # 单个连通分量  key: INT子网id, value: [INT子网id, ]
                cc_sn_ids = {}
                while stack:
                    node = stack.pop()
                    cc_sn_ids[node] = int_sn_conns[node]
                    for neighbour in int_sn_conns[node]:
                        if neighbour not in visited:
                            visited.append(neighbour)
                            stack.append(neighbour)
                ccs_sn_ids.append(cc_sn_ids)

        # 添加VPC及VPC子网
        i = 0
        int_vpc_sn = {}

        # 一个连通分量对应一个VPC
        for cc_sn_ids in ccs_sn_ids:
            i += 1
            vpc1 = HW_VPC(name='VPC'+str(i))
            vpc1.cidr = CIDR('10.'+str(i)+'.0.0/16')
            self.vpcs[vpc1.id] = vpc1
            j = 0

            # 同一连通分量里的所有子网同属一个VPC
            for int_sn_id in cc_sn_ids:
                j += 1

                vpc_sn = HW_Subnet(name='{}-子网{}'.format(vpc1.name, j))
                vpc_sn.cidr = vpc1.next_subnet_cidr()
                # has_vpc_sn.append(sn_id)
                vpc_sn.vpc_id = vpc1.id
                vpc1.subnets.append(vpc_sn.id)
                self.subnets[vpc_sn.id] = vpc_sn

                vpc_sn.int_subnet_id = int_sn_id

                # add hosts
                sn = int_nw.subnets[int_sn_id]
                for k in range(0, sn.n_hosts):
                    h = HW_Host(name='{}-主机{}'.format(vpc_sn.name, k + 1))
                    h.subnet_id = vpc_sn.id
                    vpc_sn.hosts.append(h.id)
                    self.hosts[h.id] = h

            # key: INT子网id, value: VPC子网id
            for sn_id in vpc1.subnets:
                int_vpc_sn[self.subnets[sn_id].int_subnet_id] = sn_id

            # INT子网的可达转换为VPC子网的可达

            # key: VPC子网id, value: [VPC子网id, ]
            vpc_sn_ids = {}
            for int_sn_id in cc_sn_ids:
                vpc_sn_id = int_vpc_sn[int_sn_id]
                vpc_sn_ids[vpc_sn_id] = []
                for cc_neighbour_id in cc_sn_ids[int_sn_id]:
                    neighbour_id = int_vpc_sn[cc_neighbour_id]
                    vpc_sn_ids[vpc_sn_id].append(neighbour_id)
            # vpc_sn_ids.clear()
            # vpc_sn_ids = int_vpc_conns

            # 计算每个子网的所有不可达子网, key: 子网id, value: [子网id, ]
            iso_vpc_sn = {}

            # 如果一个子网有无法到达的其他子网，则添加 ACL
            for sn_id in vpc1.subnets:
                if len(vpc_sn_ids[sn_id]) < len(vpc1.subnets)-1:
                    sn_cant_reach = list(vpc1.subnets)
                    sn_cant_reach.remove(sn_id)
                    for neighbour_id in vpc_sn_ids[sn_id]:
                        sn_cant_reach.remove(neighbour_id)
                    iso_vpc_sn[sn_id] = sn_cant_reach

            # 隔离(不可达)性去重
            remove_list = []
            for sn_id, iso_sn_ids in iso_vpc_sn.items():
                for iso_sn_id in iso_sn_ids:
                    if iso_sn_id in iso_vpc_sn:
                        if sn_id in iso_vpc_sn[iso_sn_id]:
                            remove_list.append(iso_sn_id)
                for remove_one in remove_list:
                    iso_vpc_sn[sn_id].remove(remove_one)
                remove_list.clear()

                # 添加ACL
                default_acl = None
                if len(iso_sn_ids) > 0:
                    default_acl = HW_ACL()
                    default_acl.name = 'ACL-' + str(default_acl.id)[0: 4]
                    sn = self.subnets[sn_id]
                    sn.acls.append(default_acl.id)
                    self.acls[default_acl.id] = default_acl
                for iso_sn_id in iso_sn_ids:
                    dst_sn = self.subnets[iso_sn_id]
                    add_acl_rule(default_acl, 'deny', 'ALL', sn.cidr, dst_sn.cidr)

        # 完全隔离的INT子网独属一个VPC
        for int_sn_id in no_conns_sn:
            i += 1
            j = 1
            vpc1 = HW_VPC(name='VPC' + str(i))
            vpc1.cidr = CIDR('10.' + str(i) + '.0.0/16')
            self.vpcs[vpc1.id] = vpc1

            vpc_sn = HW_Subnet(name='{}-子网{}'.format(vpc1.name, j))
            vpc_sn.cidr = vpc1.next_subnet_cidr()
            vpc_sn.vpc_id = vpc1.id
            vpc1.subnets.append(vpc_sn.id)
            self.subnets[vpc_sn.id] = vpc_sn

            vpc_sn.int_subnet_id = int_sn_id

            int_vpc_sn[int_sn_id] = vpc_sn.id

        # process loadbalancing
        lb_vpc_sn = []
        for ilb in int_nw.intents_lb.values():
            sn_id = int_vpc_sn[ilb.subnet2_id]
            if sn_id not in lb_vpc_sn:
                lb_vpc_sn.append(sn_id)

        for sn_id in lb_vpc_sn:
            default_elb = HW_ELB()
            default_elb.name = 'ELB-' + str(default_elb.id)[0:4]
            default_elb.type = 'private network'
            default_monitor = add_monitor(default_elb, 'TCP', 80)
            default_server_group = add_server_group(default_monitor, 'WRR')
            sn = self.subnets[sn_id]
            sn.elbs.append(default_elb.id)
            self.elbs[default_elb.id] = default_elb


    def __init__(self):
        self.project_id = None
        self.vpcs = {}
        self.subnets = {}
        self.hosts = {}
        self.peers = {}
        self.security_groups = {}
        self.acls = {}
        self.elbs = {}

    def __str__(self):
        result = ''''''
        for vpc in self.vpcs.values():
            result += 'VPC: <{}, cidr: {}>\n'.format(vpc.name, vpc.cidr)
            for sn_id in vpc.subnets:
                sn = self.subnets[sn_id]
                result += ' '*4 + '子网: <{}, cidr: {}>\n'.format(sn.name, sn.cidr)

                for elb_id in sn.elbs:
                    elb = self.elbs[elb_id]
                    result += ' ' * 8 + '{}: \n'.format(elb.name)
                    result += ' ' * 8 + '{} \n'.format(str(elb))
                    for monitor in elb.monitors:
                        result += ' ' * 12 + '{} \n'.format(str(monitor))
                        for server_group in monitor.server_groups:
                            result += ' ' * 16 + '{} \n'.format(str(server_group))

                for acl_id in sn.acls:
                    acl = self.acls[acl_id]
                    result += ' ' * 8 + '{}: \n'.format(acl.name)
                    for rule in acl.acl_rules:
                        result += ' ' * 12 + '{} \n'.format(str(rule))

                if len(sn.hosts) > 0:
                    result += ' '*8 + '主机: [' + '<{}>, '*(len(sn.hosts)-1) + '<{}>' + ']\n'
                for h_id in sn.hosts:
                    h = self.hosts[h_id]
                    result = result.replace('{}', h.name, 1)

        return result
