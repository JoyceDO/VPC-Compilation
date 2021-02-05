from src.defs.intents import *


class IntentNetwork(object):
    def add_subnet(self, host_number=0,name=''):
        sn = INT_Subnet()
        sn.n_hosts = host_number
        sn.n_name = name
        self.subnets[sn.id] = sn
        return sn

    '''
    def add_router(self, subnet_id=None):
        r = INT_Router()
        r.subnet_id = subnet_id
        self.routers[r.id] = r
        return r
        '''

    '''
    def add_intent_reachability(self, router, subnet):
        assert isinstance(router, INT_Router) and isinstance(subnet, INT_Subnet)
        assert router.id in self.routers and subnet.id in self.subnets
        i_r = INT_Reachability(router.id, subnet.id)
        self.intents_r[i_r.id] = i_r
        '''

    def add_intent_reachability(self, subnet1, subnet2):
        assert isinstance(subnet1, INT_Subnet) and isinstance(subnet2, INT_Subnet)
        assert subnet1.id in self.subnets and subnet2.id in self.subnets
        i_r = INT_Reachability(subnet1.id, subnet2.id)
        self.intents_r[i_r.id] = i_r

    '''
    def add_intent_isolation(self, router, subnet):
        assert isinstance(router, INT_Router) and isinstance(subnet, INT_Subnet)
        assert router.id in self.routers and subnet.id in self.subnets
        i_i = INT_Isolation(router.id, subnet.id)
        self.intents_i[i_i.id] = i_i
        '''

    def add_intent_isolation(self, subnet1, subnet2):
        assert isinstance(subnet1, INT_Subnet) and isinstance(subnet2, INT_Subnet)
        assert subnet1.id in self.subnets and subnet2.id in self.subnets
        i_i = INT_Isolation(subnet1.id, subnet2.id)
        self.intents_i[i_i.id] = i_i

    '''
    def add_intent_loadbalancing(self, router, subnet):
        assert isinstance(router, INT_Router) and isinstance(subnet, INT_Subnet)
        assert router.id in self.routers and subnet.id in self.subnets
        i_lb = INT_Loadbalancing(router.id, subnet.id)
        self.intents_lb[i_lb.id] = i_lb
        '''

    def add_intent_loadbalancing(self, subnet1, subnet2):
        assert isinstance(subnet1, INT_Subnet) and isinstance(subnet2, INT_Subnet)
        assert subnet1.id in self.subnets and subnet2.id in self.subnets
        i_lb = INT_Loadbalancing(subnet1.id, subnet2.id)
        self.intents_lb[i_lb.id] = i_lb

    def __init__(self):
        self.subnets = {}
        # self.routers = {}
        self.intents_r = {}   # reachability
        self.intents_i = {}   # isolation
        self.intents_lb = {}  # loadbalancing

    def __str__(self):
        result = ''''''
        result += '子网: \n'
        for sn in self.subnets.values():
            result += ' ' * 4 + '子网UUID: {}, 主机数量: {}\n'.format(sn.id, sn.n_hosts)
        result += '可达性: \n'
        for ir in self.intents_r.values():
            result += ' ' * 4 + '子网甲UUID: {}, 子网乙UUID: {}\n'.format(ir.subnet1_id, ir.subnet2_id)
        result += '隔离性: \n'
        for ii in self.intents_i.values():
            result += ' ' * 4 + '子网甲UUID: {}, 子网乙UUID: {}\n'.format(ii.subnet1_id, ii.subnet2_id)
        result += '负载均衡: \n'
        for ilb in self.intents_lb.values():
            result += ' ' * 4 + '子网甲UUID: {}, 子网乙UUID: {}\n'.format(ilb.subnet1_id, ilb.subnet2_id)
        return result

