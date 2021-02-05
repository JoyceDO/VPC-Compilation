import numpy as np
import copy
import math
import networkx as nx
import matplotlib.pyplot as plt

class Converter(object):
    def __init__(self):
        self.distribution = {}

        # 计算意图网中每个子网的所有可达子网，key:子网id，value:[子网id, ]
        self.connect_subnets = {}

        self.connect_subnets_temp = {}
        self.group_divide = {}

        # 计算意图网中完全独立（无可达子网）的子网
        self.isolationists = []

        #计算意图网中的连通分量
        self.ccs = []

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

    def contract(self,s_t,g,in_set,vertex_num):

        visited = np.zeros(vertex_num)
        wage = np.zeros(vertex_num)
        ans = float(0)
        for i in range(0,vertex_num):
            k = -1
            max = -1
            for j in range(0,vertex_num):
                if in_set[j] == 0 and visited[j] == 0 and wage[j] > max:
                    k = j
                    max = wage[j]
            if k == -1:
                return ans
            s_t[0] = s_t[1]
            s_t[1] = k
            ans = max
            visited[k] = 1
            for j in range(0,vertex_num):
                if in_set[j] == 0 and visited[j] == 0:
                    wage[j] = wage[j] + g[k][j]

        return ans

    def find_cut(self, vertex_list,group,final_two_nums):

        self.group_divide[group] = []
        two_nums = [0,0]
        group_temp_1 = []
        group_temp_2 = []

        group_to_divide_1 = []
        group_to_divide_2 = []

        ans = 0
        max = 0
        min_cut = float("inf")

        edges_sum = float(0)
        for subnet in self.distribution[group]:
            edges_sum += len(self.connect_subnets_temp[subnet])

        k = math.ceil((edges_sum/2)*0.3)

        j = 0

        for i in range(0,1):
            #print("lllllllllllllllllllllllll")
            ans = self.sw(vertex_list,group_temp_1,group_temp_2,two_nums,group_to_divide_1,group_to_divide_2)
            #print(ans)
            #print((two_nums[0] * two_nums[1] - ans) / ans)
            if (min_cut == float("inf") and ans < min_cut) or (two_nums[0]*two_nums[1]-ans)/ans > max:
                #print("ssssssssssssssssssssss")
                #print(ans)
                final_two_nums[0] = two_nums[0]
                final_two_nums[1] = two_nums[1]
                self.group_divide[group].clear()
                self.group_divide[group] = copy.deepcopy(group_to_divide_1)
                min_cut = ans
                max = (two_nums[0]*two_nums[1]-ans)/ans

            group_temp_1.append([])
            group_temp_2.append([])

            group_temp_1[j] = copy.deepcopy(group_to_divide_1)
            group_temp_2[j] = copy.deepcopy(group_to_divide_2)
            j += 1

        if min_cut == 0:
            return 0

        return min_cut


    '''
    def find_cut(self, vertex_list,group,two_nums):
        self.group_divide[group]= []
        group_temp = []
        #group_temp[0] = []
        #group_temp[1] = []
        group_temp.append([])
        group_temp.append([])
        min_cut = min_cut_1 = self.sw(vertex_list, group, group_temp)
        max = (len(group_temp[0])*len(group_temp[1])-min_cut_1)/min_cut_1

        self.group_divide[group] = copy.deepcopy(group_temp[0])
        two_nums[0]=len(group_temp[0])
        two_nums[1] = len(group_temp[1])
        group_first = copy.deepcopy(group_temp)
        min_cut_2 = self.sw(group_first[0],group, group_temp)
        if min_cut_2 != float("inf"):
            already_compute = 0
            for vertex in group_temp[0]:
                for connect in self.connect_subnets_temp[vertex]:
                    if connect in group_first[1]:
                        if ((len(group_temp[0])+len(group_first[1]))*len(group_temp[1])-min_cut_2)/min_cut_2 > max:
                            max = ((len(group_temp[0])+len(group_first[1]))*len(group_temp[1])-min_cut_2)/min_cut_2
                            self.group_divide[group].clear()
                            self.group_divide[group] = copy.deepcopy(group_temp[1])
                            two_nums[0] = len(group_temp[1])
                            two_nums[1] = len(group_temp[0])+len(group_first[1])
                            min_cut = min_cut_2
                        already_compute =1
                        break
            if already_compute == 0:
                for vertex in group_temp[1]:
                    for connect in self.connect_subnets_temp[vertex]:
                        if connect in group_first[1]:
                            if ((len(group_temp[1]) + len(group_first[1])) * len(
                                    group_temp[0]) - min_cut_2) / min_cut_2 > max:
                                max = ((len(group_temp[1]) + len(group_first[1])) * len(
                                    group_temp[0]) - min_cut_2) / min_cut_2
                                self.group_divide[group].clear()
                                self.group_divide[group] = copy.deepcopy(group_temp[0])
                                two_nums[0] = len(group_temp[0])
                                two_nums[1] = len(group_temp[1]) + len(group_first[1])
                                min_cut = min_cut_2
                            break
        min_cut_3 = self.sw(group_first[1], group, group_temp)
        if min_cut_3 != float("inf"):
            already_compute = 0
            for vertex in group_temp[0]:
                for connect in self.connect_subnets_temp[vertex]:
                    if connect in group_first[0]:
                        if ((len(group_temp[0])+len(group_first[0]))*len(group_temp[1])-min_cut_3)/min_cut_3 > max:
                            max = ((len(group_temp[0])+len(group_first[0]))*len(group_temp[1])-min_cut_3)/min_cut_3
                            self.group_divide[group].clear()
                            self.group_divide[group] = copy.deepcopy(group_temp[1])
                            two_nums[0] = len(group_temp[1])
                            two_nums[1] = len(group_temp[0]) + len(group_first[0])
                            min_cut = min_cut_3
                        already_compute =1
                        break
            if already_compute == 0:
                for vertex in group_temp[1]:
                    for connect in self.connect_subnets_temp[vertex]:
                        if connect in group_first[0]:
                            if ((len(group_temp[1]) + len(group_first[0])) * len(
                                    group_temp[0]) - min_cut_3) / min_cut_3 > max:
                                max = ((len(group_temp[1]) + len(group_first[0])) * len(
                                    group_temp[0]) - min_cut_3) / min_cut_3
                                self.group_divide[group].clear()
                                self.group_divide[group] = copy.deepcopy(group_temp[0])
                                two_nums[0] = len(group_temp[0])
                                two_nums[1] = len(group_temp[1]) + len(group_first[0])
                                min_cut = min_cut_3
                            break
        return min_cut
    '''

    #计算连通分量的边连通度（最小割）
    def sw(self,vertex_list,group_temp_1,group_temp_2,two_nums,group_to_divide_1,group_to_divide_2):


        group_to_divide_1.clear()
        group_to_divide_2.clear()
        #self.group_divide[group]= []
        vertex_num = len(vertex_list)

        in_set= np.zeros(vertex_num)
        g = np.zeros([vertex_num,vertex_num])

        vertex_to_number = {}
        number_to_vertex = {}
        merge = {}

        for i in range(0,vertex_num):
            vertex_to_number[vertex_list[i]] = i
            number_to_vertex[i] = vertex_list[i]
            merge[i] = []
            merge[i].append(i)

        for vertex in vertex_list:
            for connect_vertex in self.connect_subnets_temp[vertex]:
                already_has_value =0
                for j in range(0,len(group_temp_1)):
                    if (vertex in group_temp_1[j] and connect_vertex in group_temp_2[j]) or (vertex in group_temp_2[j] and connect_vertex in group_temp_1[j]):
                        g[vertex_to_number[vertex]][vertex_to_number[connect_vertex]] = 999
                        already_has_value =1
                        break
                if already_has_value ==0 :
                    g[vertex_to_number[vertex]][vertex_to_number[connect_vertex]] = 1

        min_cut = float("inf")
        ans = 0

        for i in range(1,vertex_num):
            s_t = [0, 0]
            ans = self.contract(s_t,g,in_set,vertex_num)
            in_set[s_t[1]] = 1

            if ans < min_cut or (ans == min_cut and len(merge[s_t[1]])*(vertex_num-len(merge[s_t[1]]))>two_nums[0]*two_nums[1]):
                #self.group_divide[group].clear()

                group_to_divide_1.clear()
                min_cut = ans
                two_nums[0] = len(merge[s_t[1]])
                two_nums[1] = vertex_num-two_nums[0]

                for merge_number in merge[s_t[1]]:
                    #计算删除最小割后的某一连通分量
                    #self.group_divide[group].append(number_to_vertex[merge_number])
                    group_to_divide_1.append(number_to_vertex[merge_number])




            for merge_number in merge[s_t[1]]:
                merge[s_t[0]].append(merge_number)
            merge[s_t[1]].clear()

            if min_cut == 0:
                return 0
            for j in range(0, vertex_num):
                if in_set[j] == 0:
                    g[s_t[0]][j] = g[j][s_t[0]] = (g[s_t[0]][j] + g[s_t[1]][j])

        for vertex in vertex_list:
            if vertex not in group_to_divide_1:
                group_to_divide_2.append(vertex)

        return min_cut

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

        #记录每次调整分组后的节点（子网）连接情况
        '''
        self.connect_subnets_temp = {}
        for item in self.connect_subnets:
            self.connect_subnets_temp[item]=[]
            for itemm in self.connect_subnets[item]:
                self.connect_subnets_temp[item].append(itemm)
        '''
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
            if (self.flag == 1):
                break

            for group in self.distribution:
                if group in new_groups:
                    subnets_sum = len(self.distribution[group])
                    if subnets_sum == 1 :
                        continue

                    #计算某个组的连通分量的边连通度
                    edges_connectivity = self.find_cut(self.distribution[group],group,two_nums)


                    #if edges_connectivity*2/edges_sum < 0.3:
                    priority = 0.25*(two_nums[0]*two_nums[1]-edges_connectivity)+0.75* (two_nums[0]*two_nums[1]-edges_connectivity)/edges_connectivity

                    #if priority>1.49:
                    self.priority_insert(priority_order,group,priority)

            if not priority_order:
                break

            #选取可分割组里优先级最高的进行分割
            group_to_divide = priority_order[0][0]
            #print("ooooooooooooooooooooo")
            #print(len(priority_order))
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
                #print("))))))))))))))))))))))))))")
                for other_group_index in range(divided_group[initial].index(group)+1,length):
                    #print(divided_group[initial][other_group_index])
                    already_peering =0
                    for subnet in self.distribution[group]:
                        for connect in self.connect_subnets[subnet]:
                            if connect in self.distribution[divided_group[initial][other_group_index]]:
                                #print("here......")
                                peering_now += 1
                                already_peering=1
                                break
                        if already_peering:
                            break
            #print("llllllllllllllllllllllllll")
            #print(peering_now)
            #print("????????????????")
            #print(divided_group[initial])

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
            #print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhere is the peering number")
            #print(peering_sum)
            if over_the_route_num ==1 or (peering_sum-initial_group_peering[initial]+peering_now) > 10   :
                #if over_the_route_num == 0:
                    #print("1111!!!!")
                    #print(self.distribution[group_to_divide])
                    #print(self.distribution[group_to_add])
                for subnet in self.distribution[group_to_add]:
                    self.distribution[group_to_divide].append(subnet)
                self.distribution.pop(group_to_add)
                new_groups.clear()
                del priority_order[0]
                continue

            peering_sum = peering_sum-initial_group_peering[initial]+peering_now
            #print("222222222222222222222")
            #print(peering_sum)
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

            #print("pppppppppppppppp")
            #print(self.distribution[group_to_divide])
            #print(self.distribution[group_to_add])

            #删除已分割的组
            del priority_order[0]

            self.flag = 1

    def convert_intent_network(self,int_nw,G,intsubnetid_to_subnet,pos):

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
            i = i + 1
        final_average_delay = delay_sum / connect_pair
        final_acl_nums = 0
        for group in self.distribution:
            final_acl_nums += len(self.distribution[group]) * (len(self.distribution[group]) - 1)
        for group in self.distribution:
            for subnet in self.distribution[group]:
                if subnet in self.connect_subnets:
                    for connect in self.connect_subnets[subnet]:
                        if connect in self.distribution[group]:
                            final_acl_nums -= 1

        print("initial average delay:  " + str(initial_average_delay))
        print("final average delay:  " + str(final_average_delay))
        print("the difference:   " + str(initial_average_delay - final_average_delay))
        print("initial acl nums:  " + str(initial_acl_nums))
        print("final acl nums:   " + str(final_acl_nums))
        print("the difference:   " + str(initial_acl_nums - final_acl_nums))
        # print(self.flag)
        #self.data["initial average delay"] = str(initial_average_delay)
        #self.data["final average delay"] = str(final_average_delay)
        #self.data["initial acl nums"] = str(initial_acl_nums)
        #self.data["final acl nums"] = str(final_acl_nums)
        nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='g')
        # nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        color = ['skyblue', 'grey', 'yellow', 'black', 'green', 'purple', 'pink', 'orange', 'brown', 'red', 'beige',
                 'khaki', 'blue', 'tan', 'tomato', 'papayawhip', 'palegreen', 'peru', 'plum', 'powderblue',
                 'palevioletred',
                 'royalblue', 'slateblue', 'teal', 'thistle', 'wheat', 'yellowgreen', 'sandybrown', 'seagreen',
                 'seashell',
                 'rosybrown', 'palegoldenrod']
        i = 0
        for node in graph_node_list:
            nx.draw_networkx_nodes(G, pos, nodelist=node, node_color=color[i], node_size=20)
            i = i + 1

        plt.show()
        print("group nums:" + str(len(self.distribution)))





    def __str__(self):
        result = ''''''
        for group in self.distribution:
            result += 'GROUP: <{}>\n'.format(group)
            for subnet in self.distribution[group]:
                result += ' '*4 + '子网: <id: {}>\n'.format(subnet)

        return result



