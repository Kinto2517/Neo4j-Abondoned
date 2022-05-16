from neo4j import GraphDatabase

gdb = GraphDatabase.driver(uri="neo4j+s://861e9768.databases.neo4j.io:7687", auth=("neo4j","Xif0afX2j99LMtvmU60fUO6op63RAHobYZ5pAVbYgN8"))
session = gdb.session()



q1 = "MATCH (x) return (x)"

nodes = session.run(q1)

for node in nodes:
    print(node)


