import uuid


class INT_Object(object):
    def __init__(self, name=''):
        self.id = uuid.uuid4()  # uuid形式的资源标识符
        self.name = name


class INT_Subnet(INT_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_hosts = 0  # 子网内的 host 数量
        self.n_name = ''


class INT_Reachability(INT_Object):
    # def __init__(self, router_id, subnet_id):
    def __init__(self, subnet1_id, subnet2_id):
        super().__init__()
        '''
        self.router_id = router_id
        self.subnet_id = subnet_id
        '''
        self.subnet1_id = subnet1_id
        self.subnet2_id = subnet2_id


class INT_Isolation(INT_Object):
    # def __init__(self, router_id, subnet_id):
    def __init__(self, subnet1_id, subnet2_id):
        super().__init__()
        '''
        self.router_id = router_id
        self.subnet_id = subnet_id
        '''
        self.subnet1_id = subnet1_id
        self.subnet2_id = subnet2_id


class INT_Loadbalancing(INT_Object):
    # def __init__(self, router_id, subnet_id):
    def __init__(self, subnet1_id, subnet2_id):
        super().__init__()
        '''
        self.router_id = router_id
        self.subnet_id = subnet_id
        '''
        self.subnet1_id = subnet1_id
        self.subnet2_id = subnet2_id


# End of file
