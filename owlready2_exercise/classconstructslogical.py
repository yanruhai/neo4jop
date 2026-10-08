from owlready2 import *

onto = get_ontology("http://test.org/onto.owl")

with onto:
    class Drug(Thing):
        pass
    class ActivePrinciple(Thing):
        pass
    class has_for_active_principle(Drug >> ActivePrinciple):
        pass


    class NonPlaceboDrug(Drug):
        equivalent_to = [Drug & has_for_active_principle.some(ActivePrinciple)]


    class DrugAssociation(Drug):
        equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]


onto2 = get_ontology("http://test.org/onto2.owl")

with onto2:
    class Drug(Thing): pass
    class ActivePrinciple(Thing): pass
    class has_for_active_principle(Drug >> ActivePrinciple): pass

    class HeathCondition(Thing): pass
    class Pain(HeathCondition): pass
    class ModeratePain(Pain): pass
    class CardiacDisorder(HeathCondition): pass
    class Hypertension(CardiacDisorder): pass

    class Pregnancy(HeathCondition): pass
    class Child(HeathCondition): pass
    class Bleeding(HeathCondition): pass

    class has_for_indications(Drug >> HeathCondition):
        class_property_type = ["some"]
        #是的，class_property_type 是 Owlready2 中专门保留的特殊属性（关键字/特殊配置项）。
        #它专门用来控制当你在“类对象”上直接进行属性赋值时，Owlready2 在后台如何将这些赋值转换为 OWL 描述逻辑中的限制（Restrictions）。
    class has_for_contraindications(Drug >> HeathCondition):
        class_property_type = ["only"]

    class Antalgic(Drug):
         defined_class = True
         has_for_indications = [Pain]
         has_for_contraindications = [Pregnancy, Child, Bleeding]

    class Aspirin(Antalgic):
         defined_class = True
         has_for_indications = [ModeratePain]
         has_for_contraindications = [Pregnancy, Bleeding]

print(Antalgic.equivalent_to)
