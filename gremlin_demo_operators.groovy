g = new Neo4jGraph('/home/andrei/Databases/neo4j-replica/graph.db')
g.saveGraphML('/home/andrei/testGraphML.graphml')

g.V.map
g.v(142869).outE.filter{"is_part_of_pathway"}.inV.filter{["PathwayStep","Pathway"]}.map