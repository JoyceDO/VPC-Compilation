import numpy as np
import copy
import math
from collections import deque
import random
import networkx as nx
import matplotlib.pyplot as plt

class Converter4(object):
    def __init__(self):



        # 计算意图网中每个子网的所有可达子网，key:子网id，value:[子网id, ]
        self.connect_subnets = {}

        self.connect_subnets_temp = {}
        self.group_divide = {}

        # 计算意图网中完全独立（无可达子网）的子网
        self.isolationists = []

        #计算意图网中的连通分量
        self.ccs = []

        # 记录分组前后时延与ACL规则数情况
        self.data = {}

        # key:子网id, value:子网对象
        self.subnets = {}

        # 记录分组情况 key:组号, value:[子网id, ]
        self.distribution = {}

        self.flag = 0


    def dfs(self):
        visited = []
        stack = []

        for subnet in self.connect_subnets:
            if subnet not in visited:
                visited.append(subnet)
                stack.append(subnet)

                cc = {}
                while stack:
                    node = stack.pop()
                    cc[node] = self.connect_subnets
                    for neighbour in self.connect_subnets[node]:
                        if neighbour not in visited:
                            visited.append(neighbour)
                            stack.append(neighbour)
                self.ccs.append(cc)

    def initial_distribution(self):
        i=0
        for cc in self.ccs:

            self.distribution[i] = []
            for subnet in cc:
                self.distribution[i].append(subnet)
            i += 1
        for isolationist in self.isolationists:

            self.distribution[i] = []
            self.distribution[i].append(isolationist)
            i += 1

    def contract(self,vertex, edge, num, merge, k):

        while (len(vertex) > num):
            ind = random.randrange(0, len(edge))
            u = edge[ind][0]
            v = edge[ind][1]
            vertex.remove(v)
            for merge_v in merge[v]:
                merge[u].append(merge_v)
            del merge[v]
            delete_edge = []
            for i in range(len(edge)):
                if edge[i][0] == v:
                    edge[i][0] = u
                elif edge[i][1] == v:
                    edge[i][1] = u
                if edge[i][0] == edge[i][1]:
                    delete_edge.append(edge[i])
            for edgee in delete_edge:
                edge.remove(edgee)
            del delete_edge
        return (len(edge))

    def recursive_contract(self,vertex, edge, vertex_num, minimum_cut, previous_merge, k):
        q_vertex = deque()
        q_edge = deque()
        q_merge = deque()

        initial_merge = {}
        for v in vertex:
            initial_merge[v] = []
            initial_merge[v].append(v)

        sub_size = vertex_num
        index = 1
        ans = 0

        j =1
        q_vertex.append(vertex)
        q_edge.append(edge)
        q_merge.append(initial_merge)

        while (sub_size > 6):
            #print(j)
            j = j+1
            sub_size = math.ceil(1+sub_size / math.pow(2, 1 / 2))
            for i in range(0, index):
                vertex_temp_1 = copy.deepcopy(q_vertex[0])
                edge_temp_1 = copy.deepcopy(q_edge[0])
                merge_temp_1 = copy.deepcopy(q_merge[0])
                self.contract(vertex_temp_1, edge_temp_1, sub_size, merge_temp_1, k)
                q_vertex.append(vertex_temp_1)
                q_edge.append(edge_temp_1)
                q_merge.append(merge_temp_1)

                vertex_temp_2 = copy.deepcopy(q_vertex[0])
                edge_temp_2 = copy.deepcopy(q_edge[0])
                merge_temp_2 = copy.deepcopy(q_merge[0])
                self.contract(vertex_temp_2, edge_temp_2, sub_size, merge_temp_2, k)
                q_vertex.append(vertex_temp_2)
                q_edge.append(edge_temp_2)
                q_merge.append(merge_temp_2)

                q_vertex.popleft()
                q_edge.popleft()
                q_merge.popleft()

            index = index * 2

        ans = 9999
        merge_final = []
        while (len(q_vertex) != 0):
            vertex_temp = q_vertex[0]
            edge_temp = q_edge[0]
            merge_temp = q_merge[0]
            ans_temp = self.contract(vertex_temp, edge_temp, 2, merge_temp, k)

            if ans_temp != 0 and ans_temp < ans:
                ans = ans_temp
                merge_final = merge_temp

            q_vertex.popleft()
            q_edge.popleft()
            q_merge.popleft()

        if ans == 9999:
            return

        already_exits = 0
        for key in merge_final:
            for merge in previous_merge:
                for key2 in merge:
                    if set(merge_final[key]) == set(merge[key2]):
                        already_exits = 1
                        break
                if already_exits:
                    break
            if already_exits:
                break

        if already_exits == 0:
            minimum_cut.append(ans)
            previous_merge.append(merge_final)

    def find_cut(self, vertex_list,group):

        vertex_num = len(vertex_list)

        vertexs = []
        edges = []

        vertex_to_number = {}
        number_to_vertex = {}

        G = nx.Graph()

        for i in range(0,vertex_num):
            vertex_to_number[vertex_list[i]] = i
            number_to_vertex[i] = vertex_list[i]
            vertexs.append(i)
            G.add_node(i)

        for vertex in vertex_list:
            for connect_vertex in self.connect_subnets_temp[vertex]:
                if [vertex_to_number[connect_vertex],vertex_to_number[vertex]] not in edges:
                    edges.append([vertex_to_number[vertex],vertex_to_number[connect_vertex]])
                    G.add_edge(vertex_to_number[vertex], vertex_to_number[connect_vertex])

        self.group_divide[group] = []

        #k = vertex_num/10+1
        edge_betweenness = nx.edge_betweenness_centrality(G)
        flag = 0
        for edge in edge_betweenness:
            if edge_betweenness[edge] >= 0.1 + float(vertex_num) / 10000:
                flag = 1
        if flag and vertex_num >= 100:
            k = 10
        else:
            k = vertex_num / 10 + 1

        del G

        minimal_cut = []
        previous_merge = []
        count = int(math.log(vertex_num)) * int(math.log(vertex_num))
        for i in range(0, count):
            v = copy.deepcopy(vertexs)
            e = copy.deepcopy(edges)
            self.recursive_contract(v, e, vertex_num, minimal_cut, previous_merge, k)

        if len(minimal_cut) == 0:
            return 0

        max_acl_save = 0
        max_average = 0
        index = -1

        for i in range(0,len(minimal_cut)):
            sum = 1
            for merge_vertex in previous_merge[i]:
                sum = sum * len(previous_merge[i][merge_vertex])
            if (sum-minimal_cut[i])/minimal_cut[i] > max_average:
                max_average = (sum-minimal_cut[i])/minimal_cut[i]
                max_acl_save = sum-minimal_cut[i]
                index = i
        self.group_divide[group].clear()
        for vertex_number in previous_merge[index][list(previous_merge[index].keys())[0]]:
            self.group_divide[group].append(number_to_vertex[vertex_number])

        return max_acl_save

    def priority_insert(self,priority_order,group,priority):
        if priority_order:
            i = -1
            for group_priority in priority_order:
                i += 1
                if group_priority[1]<priority:
                    priority_order.insert(priority_order.index(group_priority),(group,priority))
                    break
            if i == len(priority_order)-1:
                priority_order.append((group,priority))
        else:
            priority_order.append((group,priority))

    def reduce_acls(self):

        self.connect_subnets_temp = copy.deepcopy(self.connect_subnets)

        #记录各组被调整的顺序
        priority_order = []

        #记录每组删除最小割后两个连通分量的节点（子网）数
        two_nums = [0,0]

        #记录由于调整而得到的新组
        new_groups = []

        #在最开始，所有初始分配的组都是未经考量的新组
        for group in self.distribution:
            new_groups.append(group)

        route_num = {}

        initial_group = {}
        divided_group = {}
        initial_group_peering = {}

        peering_sum = 0

        while True:
            if(self.flag == 1):
                break

            for group in self.distribution:
                if group in new_groups:
                    subnets_sum = len(self.distribution[group])
                    if subnets_sum == 1 :
                        continue

                    priority = self.find_cut(self.distribution[group],group)
                    if priority == 0:
                        continue
                    self.priority_insert(priority_order,group,priority)

            if not priority_order:
                break

            #选取可分割组里优先级最高的进行分割
            group_to_divide = priority_order[0][0]
            group_to_add = len(self.distribution)
            self.distribution[group_to_add] = []
            over_the_route_num =0

            if group_to_divide not in initial_group:
                initial_group[group_to_divide] = group_to_divide

            if group_to_divide not in divided_group:
                divided_group[group_to_divide] = [group_to_divide]

            if group_to_divide not in initial_group_peering:
                initial_group_peering[group_to_divide] = 0


            #更新分割后的分组情况
            for subnet in self.distribution[group_to_divide]:
                if subnet not in self.group_divide[group_to_divide]:
                    self.distribution[group_to_add].append(subnet)

            self.distribution[group_to_divide].clear()
            for subnet in self.group_divide[group_to_divide]:
                self.distribution[group_to_divide].append(subnet)

            initial_group[group_to_add] = initial_group[group_to_divide]
            initial = initial_group[group_to_add]
            divided_group[initial].append(group_to_add)

            #检查如果分割对等连接数是否会超标
            peering_now = 0
            length = len(divided_group[initial])
            for group in divided_group[initial]:
                for other_group_index in range(divided_group[initial].index(group)+1,length):
                    already_peering =0
                    for subnet in self.distribution[group]:
                        for connect in self.connect_subnets[subnet]:
                            if connect in self.distribution[divided_group[initial][other_group_index]]:
                                peering_now += 1
                                already_peering=1
                                break
                        if already_peering:
                            break

            #检查如果分割对等连接路由数是否会超标
            for subnet in self.group_divide[group_to_divide]:
                if subnet not in route_num:
                    route_num[subnet] = 0
                for connect in self.connect_subnets_temp[subnet]:
                    if connect in self.distribution[group_to_add]:
                        route_num[subnet] += 1
                        if route_num[subnet]>100:
                            over_the_route_num=1
            for subnet in self.distribution[group_to_add]:
                if subnet not in route_num:
                    route_num[subnet] = 0
                for connect in self.connect_subnets_temp[subnet]:
                    if connect in self.distribution[group_to_divide]:
                        route_num[subnet] += 1
                        if route_num[subnet]>100 :
                            over_the_route_num=1

            if over_the_route_num ==1 or (peering_sum-initial_group_peering[initial]+peering_now) > 10  :
                for subnet in self.distribution[group_to_add]:
                    self.distribution[group_to_divide].append(subnet)
                self.distribution.pop(group_to_add)
                new_groups.clear()
                del priority_order[0]
                continue

            peering_sum = peering_sum-initial_group_peering[initial]+peering_now
            initial_group_peering[initial] = peering_now

            #更新分割后的连接情况
            for subnet in self.group_divide[group_to_divide]:
                for connect in self.connect_subnets_temp[subnet].copy():
                    if connect in self.distribution[group_to_add]:
                        self.connect_subnets_temp[subnet].remove(connect)
            for subnet in self.distribution[group_to_add]:
                for connect in self.connect_subnets_temp[subnet].copy():
                    if connect in self.distribution[group_to_divide]:
                        self.connect_subnets_temp[subnet].remove(connect)


            #更新分割（调整）后产生的新组
            new_groups.clear()
            new_groups.append(group_to_divide)
            new_groups.append(group_to_add)

            #删除已分割的组
            del priority_order[0]

            self.flag = 1

    def convert_intent_network(self,int_nw,G,intsubnetid_to_subnet,pos):

        self.subnets = int_nw.subnets

        #记录子网之间的可达性
        self.isolationists = list(int_nw.subnets)
        for reachability in int_nw.intents_r.values():
            subnet1_id = reachability.subnet1_id
            subnet2_id = reachability.subnet2_id

            if subnet1_id not in self.connect_subnets:
                self.connect_subnets[subnet1_id] = []
                self.isolationists.remove(subnet1_id)
            self.connect_subnets[subnet1_id].append(subnet2_id)

            if subnet2_id not in self.connect_subnets:
                self.connect_subnets[subnet2_id] = []
                self.isolationists.remove(subnet2_id)
            self.connect_subnets[subnet2_id].append(subnet1_id)

            #计算意图网里的连通分量
        self.dfs()

            #初始分配，每个连通分量对应一个VPC
        self.initial_distribution()
        initial_average_delay = 150
        initial_acl_nums = 0
        for group in self.distribution:
            initial_acl_nums += len(self.distribution[group]) * (len(self.distribution[group])-1)
        for group in self.distribution:
            for subnet in self.distribution[group]:
                if subnet in self.connect_subnets:
                    initial_acl_nums -= len(self.connect_subnets[subnet])

            #按照某种启发式规则，最大程度地减小ACL规则数量
        self.reduce_acls()
        connect_pair = 0
        delay_sum = float(0)
        divided_connected_pair = 0

        graph_node_list = []
        i = 0
        for group in self.distribution:
            graph_node_list.append([])
            for subnet in self.distribution[group]:
                graph_node_list[i].append(intsubnetid_to_subnet[subnet])
                if subnet in self.connect_subnets:
                    for connect in self.connect_subnets[subnet]:
                        connect_pair += 1
                        if connect in self.distribution[group]:
                            delay_sum += 150
                        else:
                            delay_sum += 330
                            divided_connected_pair += 1
            i =i+1
        final_average_delay = delay_sum/connect_pair
        final_acl_nums = 0
        for group in self.distribution:
            final_acl_nums += len(self.distribution[group]) * (len(self.distribution[group])-1)
        for group in self.distribution:
            for subnet in self.distribution[group]:
                if subnet in self.connect_subnets:
                    for connect in self.connect_subnets[subnet]:
                        if connect in self.distribution[group]:
                            final_acl_nums -= 1

        print("initial average delay:  "+str(initial_average_delay))
        print("final average delay:  " + str(final_average_delay))
        print("the difference:   " + str(initial_average_delay - final_average_delay))
        print("initial acl nums:  " + str(initial_acl_nums))
        print("final acl nums:   "+str(final_acl_nums))
        print("the difference:   " + str(initial_acl_nums - final_acl_nums))
        self.data["initial average delay"] = str(initial_average_delay)
        self.data["final average delay"] = str(final_average_delay)
        self.data["initial acl nums"] = str(initial_acl_nums)
        self.data["final acl nums"] = str(final_acl_nums)

        nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='g')
        #nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        color = ['skyblue', 'grey', 'yellow', 'black', 'green', 'purple', 'pink', 'orange', 'brown', 'red', 'beige',
                 'khaki', 'blue', 'tan', 'tomato','papayawhip','palegreen','peru','plum','powderblue','palevioletred',
                 'royalblue','slateblue','teal','thistle','wheat','yellowgreen','sandybrown','seagreen','seashell',
                 'rosybrown','palegoldenrod']
        i = 0
        for node in graph_node_list:
            nx.draw_networkx_nodes(G, pos, nodelist=node, node_color=color[i],node_size=20)
            i = i + 1

        plt.show()
        print("group nums:"+str(len(self.distribution)))





    def __str__(self):
        result = ''''''
        for group in self.distribution:
            result += 'GROUP: <{}>\n'.format(group)
            for subnet in self.distribution[group]:
                result += ' '*4 + '子网: <id: {}>\n'.format(subnet)

        return result