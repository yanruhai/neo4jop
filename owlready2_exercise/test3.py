from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    class Drug(Thing): pass
    class has_dosage_mg(Drug >> int, FunctionalProperty): pass


    class Ingredient(Thing):
        pass

    class has_for_ingredient(ObjectProperty):
        domain = [Drug]
        range = [Ingredient]

    class test_for_ingredient(FunctionalProperty):
        pass

# 1. 第一次调用：创建名为 "aspirin" 的节点
d1 = Drug("aspirin", namespace = onto, has_dosage_mg = 100)
print(d1, d1.has_dosage_mg)
# 输出: test.aspirin 100

# 2. 第二次调用：传入相同的 name 和 namespace，但改了剂量参数
d2 = Drug("aspirin", namespace = onto, has_dosage_mg = 500)

# 3. 验证结果
print(d2, d2.has_dosage_mg)
# 输出: test.aspirin 500 （属性已被更新）

# 4. 证明 d1 和 d2 是否是内存中的同一个实体对象：
print(d1 is d2)
# 输出: True （没有创建重复对象，d1 和 d2 对应同一个内存对象和图节点！）
print(has_for_ingredient.domain)
my_drug=Drug('my_drug')
acetaminophen = Ingredient("acetaminophen")
my_drug.has_for_ingredient=[acetaminophen]#成员名反射
print(type(my_drug.has_for_ingredient))