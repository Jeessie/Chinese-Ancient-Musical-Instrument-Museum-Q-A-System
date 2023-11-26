from py2neo import Graph, Node, Relationship,NodeMatcher,RelationshipMatcher
import json

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')
matcher = NodeMatcher(graph)
relationshipmatcher=RelationshipMatcher(graph)
def query_graph(query):
    data = graph.run(query).data()

    node_ids = {}
    new_nodes = []
    new_links = []
    for a in data:
        for tk,tv in a.items():
            nodes = tv.nodes
            relations = tv.relationships
        for n in nodes:
            if n.identity in node_ids.keys():
            #if node_ids.has_key(n.identity):
                continue
            else:
                obj = {}
                #obj["id"] = n.identity
                if n.labels is not None:

                    for la in n.labels:
                        #print(la)
                        obj["category"] = 0
                        obj['symbolSize']=70
                        if la=='Museum':
                            obj["category"] = 1
                            obj['symbolSize'] = 50
                        elif la=='Person':
                            obj["category"] = 2
                            obj['symbolSize'] = 50
                for k,v in n.items():
                    if k=='名称' or k=='博物馆' or k=='人物':
                        obj["name"]=v
                    #else:
                    #   obj[k] = v
                node_ids[n.identity]=obj["name"]
                new_nodes.append(obj)
        for r in relations:
            if r.identity in node_ids:
                continue
            li = {}
           # li["id"] = r.identity
            #if r.types() is not None:
             #   li["label"] = []
            for la in r.types():
                #li["label"].append(la)
                li["name"]=la
                sid=r.start_node.identity
                endid=r.end_node.identity
                li["source"] = node_ids[sid]
                li["target"] = node_ids[endid]
            for k,v in r.items():
                li['des'] = v
            node_ids[n.identity]=obj["name"]
            new_links.append(li)
    result = {}
    result["data"] = new_nodes
    result["links"] = new_links
    return result

files=['D:/Museum-query/Museum_query_system/Museum_QA/code/dict/exhibits_name_pos.txt', 'D:/Museum-query/Museum_query_system/Museum_QA/code/dict/museum_pos.txt','D:/Museum-query/Museum_query_system/Museum_QA/code/dict/person_pos.txt']
kindlist=['Exhibits','Museum','Person']
namelist=['名称','博物馆','人物']

#查询全部
def searchall():
    result = query_graph("MATCH (m)<-[rel]->(n)return rel")
    return result

#输入名字，查询节点和关系
def findsearch(value):
    kind=findlables(value)
    if kind==0:
        result=query_graph("MATCH(p:Exhibits{名称:'"+value+"'})<-[rel]->(n) RETURN rel")
    elif kind==1:
        result = query_graph("MATCH(p:Museum{博物馆:'" + value + "'})<-[rel]->(n) RETURN rel")
    elif kind==2:
        result = query_graph("MATCH(p:Person{人物:'" + value + "'})<-[rel]->(n) RETURN rel")
    else:
        return {"data":[],"links":[]}
    return result

#返回数字0，1，2 联动列表kindlist,namelist
def findlables(value):
    data = graph.run("match (p{名称:'" + value + "'})return labels(p)").data()
    if len(data)==0:
        data = graph.run("match (p{博物馆:'" + value + "'})return labels(p)").data()
        if len(data) == 0:
            data = graph.run("match (p{人物:'" + value + "'})return labels(p)").data()
            if len(data) == 0:
                return None
            else:
                return 2
        else:
            return 1
    else:
        return 0

#返回node，输入字符串和名字
def findnode(kind,value):
    if kind == "Exhibits":
        node = matcher.match(kind).where(名称=value).first()
    elif kind == "Museum":
        node = matcher.match(kind).where(博物馆=value).first()
    elif kind == "Person":
        node = matcher.match(kind).where(人物=value).first()
    return node

#增加一个结点
def addonenode(kind,value):
    i = findlables(value)
    result = {"data": [], "links": []}
    if i == None or kindlist[i] != kind:
        if kind == "Exhibits":
            with open(files[0], "a+", encoding='utf-8') as f:
                node1 = Node('Exhibits', 名称=value)  # 修改的部分
                graph.create(node1)
                f.write('\n'+value + " ne")
            result = query_graph("MATCH(p:Exhibits{名称:'" + value + "'})RETURN p")
        elif kind == "Museum":
            with open(files[1], "a+", encoding='utf8') as f:
                node1 = Node('Museum', 博物馆=value)  # 修改的部分
                graph.create(node1)
                f.write('\n'+value + " nmuseum")
            result = query_graph("MATCH(p:Museum{博物馆:'" + value + "'})RETURN p")
        elif kind == "Person":
            with open(files[2], "a+", encoding='utf8') as f:
                node1 = Node('Person', 人物=value)
                graph.create(node1)
                f.write('\n'+value + " np")
            result = query_graph("MATCH(p:Person{人物:'" + value + "'})RETURN p")
    elif kindlist[i] == kind:
        result = query_graph("MATCH(p:" + kind + "{" + namelist[i] + ":'" + value + "'})RETURN p")
    return result

#增加关系
def Addrelationship(kind1,value,kind2):
    value1 = value.split("；")
    # print(value1)
    addonenode(kind1, value1[0])
    addonenode(kind2, value1[2])
    node1 = findnode(kind1, value1[0])
    node2 = findnode(kind2, value1[2])
    node_1_rel_node_2 = Relationship(node1, value1[1], node2)
    graph.create(node_1_rel_node_2)
    result = findsearch(value1[0])
    return result

def findrelation(kind,value):
    #kind = findlables(value)
    if kind == 0:
        result = query_graph("MATCH(p:Exhibits{名称:'" + value + "'})-[rel]->(n) RETURN rel")
    elif kind == 1:
        result = query_graph("MATCH(p:Museum{博物馆:'" + value + "'})-[rel]->(n) RETURN rel")
    elif kind == 2:
        result = query_graph("MATCH(p:Person{人物:'" + value + "'})-[rel]->(n) RETURN rel")
    else:
        return {"data": [], "links": []}
    return result

#删除结点，包括关系
def deletenode(value):
    i=findlables(value)  #i是下标，kindlist[i]才是字符串
    node=findnode(kindlist[i],value)
    # 有关系的结点无法删除，所以先看此结点是否有关系，如果有，先删掉关系，再删除节点
    result=findrelation(i,value)
    l=len(result["links"])
    while l>0:
        c = relationshipmatcher.match((node,))
        graph.separate(c.first())
        print('删除关系成功')
        l=l-1
    graph.delete(node)  # a代表前面已经定义的结点
    if i==0:
        f = open(files[0], "r", encoding='utf8')
        a = f.readlines()
        w = open(files[0], "w", encoding='utf8')
        for line in a:
            if value not in line:
                w.write(line)
        f.close()
        w.close()
    elif i==1:
        f = open(files[1], "r", encoding='utf8')
        a = f.readlines()
        w = open(files[1], "w", encoding='utf8')
        for line in a:
            if value not in line:
                w.write(line)
        f.close()
        w.close()
    elif i==2:
        f = open(files[2], "r", encoding='utf8')
        a = f.readlines()
        w = open(files[2], "w", encoding='utf8')
        for line in a:
            if value not in line:
                w.write(line)
        f.close()
        w.close()
    return searchall()


#清空数据库
def deleteall():
    graph.delete_all()


