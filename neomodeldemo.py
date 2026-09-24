from neomodel import (
    config, StructuredNode,StructuredRel, JSONProperty,
    StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom,DateTimeProperty
)

# 1. 配置 Neo4j 数据库连接 (用户名:密码@主机:端口)
config.DATABASE_URL = "bolt://neo4j:05546644556@localhost:7687"

class Wrote(StructuredRel):
    write_time=DateTimeProperty()

# 定义 Author 节点
class Author(StructuredNode):
    name = StringProperty(required=True, unique_index=True)

    # 定义指向 Paper 的关系 (Author -> WROTE -> Paper)
    wrote = RelationshipTo('Paper', 'WROTE',model=Wrote)


# 定义 Paper 节点 (继承 SemiStructuredNode 支持动态属性)
class Paper(StructuredNode):
    paper_id = IntegerProperty(unique_index=True, required=True)
    title = StringProperty(required=True)
    category = StringProperty(default="General")
    extra_attributes = JSONProperty()
    # 反向关联 Author (Paper <- WROTE <- Author)
    authors = RelationshipFrom('Author', 'WROTE')
    # 指向其他 Paper 的 CITES 关系
    cites = RelationshipTo('Paper', 'CITES')



# 使用示例
paper = Paper(paper_id=101, title="Attention Is All You Need").save()

# 随时赋值任意深度的动态数据
paper.extra_attributes = {
    "journal": "NeurIPS",
    "citations": 50000,
    "tags": ["Transformer", "Deep Learning"]
}
paper.save()
#   model结束

def tt(a:13):
    return a

# ==========================================
# C - Create (创建)
# ==========================================

# 1. 创建单个节点 (记得调用 .save())
paper1 = Paper(paper_id=101, title="Attention Is All You Need", category="NLP").save()
paper2 = Paper(paper_id=102, title="BERT: Pre-training of Deep Bidirectional Transformers", category="NLP").save()

author1 = Author(name="Ashish Vaswani").save()
author2 = Author(name="Jacob Devlin").save()

# 2. 动态添加属性 (SemiStructuredNode 特性)
paper1.journal = "NeurIPS"
paper1.save()

# 3. 建立关系 (.connect())
author1.wrote.connect(paper1)
author2.wrote.connect(paper2)
paper2.cites.connect(paper1)  # BERT 引用了 Attention


# ==========================================
# R - Read (查询)
# ==========================================

# 1. 根据唯一索引精准获取 (查不到会抛出 Paper.DoesNotExist 异常)
p1 = Paper.nodes.get(paper_id=101)
print(f"查找到论文: {p1.title}, 动态属性 journal: {getattr(p1, 'journal', None)}")

# 2. 查找并获取（安全模式，查不到返回 None）
p_none = Paper.nodes.get_or_none(paper_id=999)

# 3. 条件过滤查询 (类似 Django ORM 语法)
nlp_papers = Paper.nodes.filter(category="NLP")
print(f"NLP 类别论文数量: {len(nlp_papers)}")

# 4. 沿着关系链查询
vaswani = Author.nodes.get(name="Ashish Vaswani")
his_papers = vaswani.wrote.all()  # 获取该作者写过的所有论文
print(f"Vaswani 写的论文: {[p.title for p in his_papers]}")


# ==========================================
# U - Update (更新)
# ==========================================

# 1. 修改属性并保存
paper1.title = "Attention Is All You Need (Updated Version)"
paper1.save()

# 2. 动态添加/删除节点 Label
paper1.add_label("HighlyCited")
paper1.remove_label("HighlyCited")

# 3. 更新关系：断开旧关系，建立新关系
# author1.wrote.disconnect(paper1)


# ==========================================
# D - Delete (删除)
# ==========================================

# 1. 断开特定关系
paper2.cites.disconnect(paper1)

# 2. 删除指定节点 (.delete())
# 注意：如果节点有外键/关系阻碍，neomodel 会自动清除其相关关系后再删除该节点
paper2.delete()
author2.delete()

print("CRUD 操作示范完成！")