from torch_geometric.datasets import Planetoid
from neo4j import GraphDatabase

# ==========================================
# 1. 加载 PyG 中的 Cora 数据集
# ==========================================
print("正在加载 PyG Cora 数据集...")
dataset = Planetoid(root='./data/Cora', name='Cora')
data = dataset[0]

num_nodes = data.num_nodes
edge_index = data.edge_index.numpy()  # 形状为 [2, num_edges]
labels = data.y.numpy()
'''
ind.cora.x：训练集节点的特征向量。
ind.cora.tx：测试集节点的特征向量。
ind.cora.allx：有标签和无标签的节点特征集合。
ind.cora.y / ind.cora.ty / ind.cora.ally：对应的节点标签（One-hot 编码）。
ind.cora.graph：以字典/邻接表形式存储的图连接关系（边）。
ind.cora.test.index：测试集节点的索引编号。
'''
# ==========================================
# 2. 配置 Neo4j 连接信息
# ==========================================
URI = "bolt://localhost:7687"  # 如果是第二个实例，修改为对应的端口（如 7688）
AUTH = ("neo4j", "05546644556")  # 替换为你的 Neo4j 数据库密码

driver = GraphDatabase.driver(URI, auth=AUTH)


# ==========================================
# 3. 写入数据到 Neo4j
# ==========================================
def import_cora_to_neo4j(tx):
    # (A) 清空旧数据（可选，防止重复导入）
    tx.run("MATCH (n) DETACH DELETE n")

    # (B) 批量创建节点 (Paper 节点)
    print("正在创建 Paper 节点...")
    # 构造节点列表：每个节点包含 id 和 label (论文类别)
    nodes_data = [
        {"id": i, "label": int(labels[i])}
        for i in range(num_nodes)
    ]
    # 使用 UNWIND 语法进行高效批量插入
    tx.run("""
        UNWIND $nodes AS node
        CREATE (:Paper {id: node.id, label: node.label})
    """, nodes=nodes_data)

    # (C) 批量创建关系 (CITES 引用关系)
    print("正在创建 CITES 引用关系...")
    edges_data = [
        {"source": int(edge_index[0, i]), "target": int(edge_index[1, i])}
        for i in range(edge_index.shape[1])
    ]
    tx.run("""
        UNWIND $edges AS edge
        MATCH (source:Paper {id: edge.source})
        MATCH (target:Paper {id: edge.target})
        CREATE (source)-[:CITES]->(target)
    """, edges=edges_data)


# 执行事务
with driver.session() as session:
    session.execute_write(import_cora_to_neo4j)

driver.close()
print("🎉 Cora 数据集成功全部导入至 Neo4j 数据库！")