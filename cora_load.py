import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid

# 1. 下载并加载数据集（以 Cora 为例）
dataset = Planetoid(
    root='./data/Cora',             # 本地保存路径
    name='Cora',                    # 可选：'Cora', 'CiteSeer', 'PubMed'
    transform=T.NormalizeFeatures() # 可选：特征归一化预处理
)

# 2. 获取图数据对象（Planetoid 仅包含 1 张图）
data = dataset[0]

# 3. 查看数据集概况
print(f"节点数量: {data.num_nodes}")
print(f"边数量: {data.num_edges}")
print(f"特征维度: {dataset.num_features}")
print(f"类别数量: {dataset.num_classes}")