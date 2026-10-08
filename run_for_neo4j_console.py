from neomodel import config, get_config,db

#用于直接运行neo4j的命令的类
config=get_config()
config.database_url = "bolt://neo4j:cloudtian101@localhost:7687"

cypher_sql1 = """
// 1. 匹配目标 OntoClass 节点和所有 :graph1 节点
MATCH (target:OntoClass {name:"graph1"})
MATCH (node:graph1)
WHERE node.city IS NOT NULL

// 2. 动态把 n.name 的值加为节点的新 Label
SET node:location
// 3. 建立原节点到 OntoClass 节点的关联关系
MERGE (node)-[r:BELONGS_TO]->(target)

// 4. 清理旧的 name 属性与旧的 graph1 标签
REMOVE node:graph1

RETURN count(node) AS processed_count;
"""

cypher_sql = """
MATCH (n:OntoClass)
WHERE n.country IS NULL
SET n.country = "USA"
RETURN count(n) AS updated_count;
"""

#<id>: 4:9ddb3220-ae6b-492b-9078-70b4d3345d22:8
params = {'elem_id': '4:9ddb3220-ae6b-492b-9078-70b4d3345d22:15'}

# 3. 发送命令并获取结果
results, meta = db.cypher_query(cypher_sql, params)


for re in results:
    print("【results 的内容】:", re[0])