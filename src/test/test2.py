import community2 as community_louvain2
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import csv

subnets = []
connect = []
isolation = []
columnb = []
columnc = []
with open('../../subnet2subnetIntent_default.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if row[0] == "PolicyType.Reachability":
            connect.append([row[1],row[2]])
        if row[0] == "PolicyType.Isolation":
            isolation.append([row[1],row[2]])
        if row[0] != "type" and row[3]=="0":
            columnb.append(row[1])
            columnc.append(row[2])

for i in range(0,len(columnb)):
    if columnb[i] not in subnets:
        subnets.append(columnb[i])

for i in range(0, len(columnc)):
    if columnc[i] not in subnets:
        subnets.append(columnc[i])

'''
count = 0
for subnet in subnets:
    if subnet[0]=='1' and subnet[1] == '2' and subnet[2] == '5' and (subnet[len(subnet)-1]=='6' or subnet[len(subnet)-1]=='7'):
        print(subnet)
        #set1.add(subnet[0:3])
        print(subnets.index(subnet))
        count+=1
print(count)
'''


dict1 = {}
#dict2 = {}
min = 300
max = 0
for subnet in subnets:
    dict1[subnet] = set()
    #dict1[subnet].add(subnet)
    #dict2[subnet] = set()
for con in connect:
    dict1[con[0]].add(con[1])

count = 0
for key in dict1:
    for con in dict1[key]:
        if key in dict1[con]:
            count +=1
print("0000000000000000000")
print(count)
'''
result = []
flag = 0
for subnet in subnets:
    flag = 0
    temp = []
    print(subnet)
    print("--------------------------")
    for s in dict1:
        if dict1[s]==dict1[subnet]:
            temp.append(s)
            #if s == "125.20.111.224/27":
            #    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(s)
    for r in result:
        if set(r)==set(temp):
            flag = 1
            break
    if flag == 0:
        result.append(temp)

    print("----------------------------")
    print("                             ")


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(result)
print(len(result))
count = 0
for r in result:
    if len(r)>1:
        print(len(r))
        print(len(dict1[r[0]]))
        print("============")
'''

'''
    print(len(dict1[subnet]))
    if len(dict1[subnet])<min:
        min = len(dict1[subnet])
    if len(dict1[subnet])>max:
        max = len(dict1[subnet])
print("``````````````````")
print(max)
print(min)
'''
'''
print(subnets[107])
print("====================")
count = 0
set1 = set()
set2 = set()
for item in dict1[subnets[107]]:
    if item[0]=='1' and item[1] == '2' and item[2] == '5' and (item[len(item)-1]=='2' or item[len(item)-1]=='4'):
        set1.add(item)
        count += 1
        print(item)
print(count)
'''
'''
count = 0
for item in dict1[subnets[2]]:
    if item[0] == '1' and item[1] == '2' and item[2] == '4':
        set2.add(item)
        count += 1
        print(item)
print(count)
if set1 == set2:
    print("~~~~~~~~~~~~")
'''


'''
# load the karate club graph

G = nx.DiGraph()
i = 0
subnet_to_node = {}
for subnet in subnets:
    G.add_node(i)
    subnet_to_node[subnet] = i
    i = i+1
for con in connect:
    G.add_edge(subnet_to_node[con[0]],subnet_to_node[con[1]])
pos = nx.spring_layout(G)
#nx.draw(G,pos,with_labels= True)
nx.draw_networkx_nodes(G, pos, node_color='y',node_size= 15)
nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='g')
plt.show()
'''

