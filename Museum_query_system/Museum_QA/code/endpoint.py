from py2neo import Graph

class neo:
    def __init__(self,endpoint_url='http://localhost:7474/'):
        self.graph = Graph(endpoint_url, auth=("neo4j", "neo4j"))

    def get_result(self,query):
        pass