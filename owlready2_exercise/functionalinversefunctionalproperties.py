from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    class Drug(Thing):
        pass


    class Ingredient(Thing):
        pass
    class has_for_cost(DataProperty, FunctionalProperty): # Each drug has a single cost
        domain    = [Drug]
        range     = [float]


    class prop(ObjectProperty): pass


    class A(Thing): pass


    class B(Thing):
        is_a = [prop.max(1)]
    # B 是一个节点类型（继承自 Thing），但我们给这种类型的节点加上了一道限制规则——从它出发的 prop 类型的边，数量不能超过 1 条
    # 等价于class B(Thing, prop.max(1))

    class ActivePrinciple(Ingredient):
        pass


    class has_for_ingredient(Drug >> Ingredient):
        pass

    class has_for_active_principle(has_for_ingredient):
        domain = [Drug]
        range = [ActivePrinciple]

my_drug=Drug()
my_drug.has_for_cost = 4.2

print(my_drug.has_for_cost)
my_drug2=Drug()
print(my_drug2.has_for_cost)

print(A().prop)

#=======================
