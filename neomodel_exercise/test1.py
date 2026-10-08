from neomodel import db, get_config

# 执行原生 Cypher 查看周边节点的真实 Label
query = """
MATCH ()-[r:BELONGS_TO]->()
WHERE r.namea IS NOT NULL
REMOVE r.namea
RETURN count(r) AS deleted_count;
"""

config = get_config()
config.database_url = "bolt://neo4j:cloudtian101@localhost:7687"

results, _ = db.cypher_query(query)

for row in results:
    print(f"实例节点名: {row[0]} | 真实 Label: {row[1]} | 关系类型: {row[2]}")