# 1. 设置数据库连接字符串 (格式: bolt://用户名:密码@主机名:端口)
from neomodel import get_config
from neomodel_exercise.model.models import Graph1

config=get_config()
config.database_url = "bolt://neo4j:cloudtian101@localhost:7687"

# ---------------- 下面就可以正常调用了 ----------------

# 2. 查询所有 person 属性为 True 的节点
person_nodes = Graph1.nodes

for node in person_nodes:
    print(f"节点 Name: {node.name}, Person 状态: {node.person}")

# 3. 更新 Sally 节点的属性
'''sally = Graph1.nodes.get(name="Sally")
sally.person = False
sally.save()'''
