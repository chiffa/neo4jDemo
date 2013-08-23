'''
Created on 20 August 2013

@author: Andrei
'''
from bulbs.neo4jserver import Graph as Neo4jGraph
from bulbs.neo4jserver import Config, NEO4J_URI, FulltextIndex
import NodeRelTypes as DDT

class Graph(Neo4jGraph):
    
    def __init__(self, config=None):
        super(Graph, self).__init__(config)
        
        #Annotations
        self.Person=self.build_proxy(DDT.Person)
        self.AnnotNode=self.build_proxy(DDT.AnnotNode)
        self.Organisation=self.build_proxy(DDT.Organisation)
        self.Handle=self.build_proxy(DDT.Handle)
        self.belongs_to=self.build_proxy(DDT.belongs_to)
        self.describes=self.build_proxy(DDT.describes)
        self.MailingList=self.build_proxy(DDT.MailingList)

Graph.default_index = FulltextIndex 
config = Config(NEO4J_URI)
config.vertex_index = "fulltext_vertex"
config.edge_index = "fulltext_edge"
DatabaseGraph=Graph(config)