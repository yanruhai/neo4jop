from neo4j import GraphDatabase
import torch
from torch_geometric.datasets import Planetoid


# 连接地址，默认端口7687；账号默认neo4j，密码是你安装时设置的密码
uri = "bolt://localhost:7687"
user = "neo4j"
password = "cloudtian101"

# 创建驱动（全局只创建1个，不要每次查询新建）
driver = GraphDatabase.driver(uri, auth=(user, password))

def close_driver():
    driver.close()

# 示例1：执行Cypher，查询
def get_person(name):
    with driver.session() as session:
        res = session.run("MATCH (p:Person {name:$name}) RETURN p.name AS name", name=name)
        record = res.single()
        if record:
            return record["name"]
    return None

# 示例2：MERGE创建节点（参数$name，防止注入！不要字符串拼接）
def create_person(name):
    with driver.session() as session:
        res = session.run(
            "MERGE (p:Person {name:$name}) RETURN p",
            name=name
        )
        return res.single()

# 示例3：MATCH + MERGE 创建关系（就是你刚才练习的那条Cypher）
def create_born_in_rel(person_name, city_name, year):
    cypher = """
        MATCH (a:Person {name:$p_name}), (b:Location {city:$city})
        MERGE (a)-[r:BORN_IN]->(b)
        ON CREATE SET r.year = $year
        ON MATCH SET r.year = $year
        RETURN r
    """
    with driver.session() as session:
        res = session.run(cypher, p_name=person_name, city=city_name, year=year)
        return res.single()

if __name__ == "__main__":
    #print(get_person("Steve"))
    create_person("yan")
    create_born_in_rel("yan", "Lynn", 1970)
    close_driver()
