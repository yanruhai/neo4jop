from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    class Drug(Thing): pass
    class ActivePrinciple(Thing): pass
    class has_for_active_principle(ObjectProperty):
        domain = [Drug]
        range  = [ActivePrinciple]
    class Analgesic(ActivePrinciple): pass     # 镇痛成分 (子类)
    class Antibiotic(ActivePrinciple): pass    # 抗生素成分 (子类)

    # 1. 父类实例 vs 子类实例
    p1 = ActivePrinciple("generic_p")
    p2 = Analgesic("aspirin")

    # 2. 两个兄弟子类的实例
    p3 = Antibiotic("penicillin")


    class DrugAssociation(Drug):
        equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]

    # 测试药物添加了父类 p1 和子类 p2
    my_drug = Drug("test_drug")
    my_drug.has_for_active_principle.extend([p1, p2])

# 推理结果：
sync_reasoner()
print("父类与子类组合，推理机认为是复方药吗:", isinstance(my_drug, DrugAssociation))
# 输出: False！(因为 p1 和 p2 依然可能指代同一实体)