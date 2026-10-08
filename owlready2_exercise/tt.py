import torch
import torch.nn as nn
import torch.nn.functional as F

logits = torch.tensor([[2.0, 1.0, 0.1]])
# 预测概率分布
probs = F.softmax(logits, dim=-1) # [0.659, 0.242, 0.099]

# 软标签分布 (软目标)
soft_targets = torch.tensor([[0.8, 0.15, 0.05]])

# 计算广义交叉熵损失：- sum( y * log(y_hat) )
loss = -torch.sum(soft_targets * torch.log(probs), dim=-1)
print(loss)

# 或者直接使用 PyTorch 的 CrossEntropyLoss (支持传入概率分布 targets)
criterion = nn.CrossEntropyLoss()
loss_official = criterion(logits, soft_targets)
print(loss_official)