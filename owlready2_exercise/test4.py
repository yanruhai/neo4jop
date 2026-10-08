from owlready2 import *

onto = get_ontology("http://example.org/drug.owl")

with onto:
    class Drug(Thing): pass
    class ActivePrinciple(Thing): pass
    class has_for_active_principle(ObjectProperty):
        domain = [Drug]
        range  = [ActivePrinciple]

    class DrugAssociation(Drug):
        equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]

    pill_a = Drug("Aspirin_C_Pill")
    p1 = ActivePrinciple("Aspirin")
    p2 = ActivePrinciple("Vitamin_C")

    # 关键点 1：明确告诉推理机 p1 和 p2 是完全不同的实体！
    AllDifferent([p1, p2])

    # 1 个成分时
    pill_a.has_for_active_principle.append(p1)

sync_reasoner(infer_property_values=True)
print("1 个成分时，是否是复方药:", isinstance(pill_a, DrugAssociation))  # False

# 追加第 2 个成分
pill_a.has_for_active_principle.append(p2)

sync_reasoner(infer_property_values=True)
print("2 个成分时，是否是复方药:", isinstance(pill_a, DrugAssociation))  # True!