from owlready2 import *

onto = get_ontology("http://example.org/demo.owl")

with onto:
    class Person(Thing): pass


    class Student(Person): pass  # Student is_a Person


    # 实例化节点
    p1 = Person("Alice")
    s1 = Student("Bob")

# 1. 查询属于 Person 类及其所有子类的【所有实例】
'''all_persons = onto.Person.instances()
print(all_persons)'''
# 输出: [demo.Alice, demo.Bob]  (Bob 是 Student，但也属于 Person 的实例)

print(p1.name)
p2=Person()
print(p2.name)

# 2. 如果只想要【精确属于该类】的实例（不包含子类），可以用列表推导式过滤：
exact_persons = [x for x in onto.Person.instances() if onto.Person in x.is_a]
print(exact_persons)
# 输出: [demo.Alice]