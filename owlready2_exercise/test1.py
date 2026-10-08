from owlready2 import *

# 定义本体的命名空间 URI（类似于数据库的 schema 名称）
onto = get_ontology("http://example.org/domain_ontology.owl")

with onto:
    # 顶级概念
    class Entity(Thing): pass

    # 一级子类：继承自 Entity
    class Person(Entity): pass


    class Organization(Entity): pass


    # 二级子类：继承自 Person
    class Student(Person): pass


    class Teacher(Person): pass

a1=Person('张三')
a2=Student('李四')
for x in (Organization.ancestors()):
    print(x.name)
