from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    # 1. 定义基础类与关系
    class a(Thing): pass


    class c(Thing): pass


    # 定义 a -b-> c
    class b(ObjectProperty):
        domain = [a]
        range = [c]


    # 2. 定义继承类：d 继承 a, e 继承 c
    class d(a): pass


    class e(c): pass


    # 3. 实例化 d 的对象 inst_d 和 e 的对象 inst_e
    inst_d = d("inst_d")
    inst_e = e("inst_e")

    # 4. 在 inst_d 和 inst_e 之间建立关系 b
    inst_d.b.append(inst_e)

# 运行推理机进行合法性与继承检查
sync_reasoner()

# 验证结果
print("1. inst_d 的关系 b 中是否有 inst_e:", inst_e in inst_d.b)  # 输出: True
print("2. inst_d 是不是 a 的实例:", isinstance(inst_d, a))  # 输出: True
print("3. inst_e 是不是 c 的实例:", isinstance(inst_e, c))  # 输出: True