from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    class Drug(Thing):
        pass


    class Ingredient(Thing):
        pass


    class has_for_ingredient(ObjectProperty):
        domain = [Drug]
        range = [Ingredient]

    class is_ingredient_of(ObjectProperty):
        domain           = [Ingredient]
        range            = [Drug]
        inverse_property = has_for_ingredient#预定义字段，关键字


my_drug2 = Drug("my_drug2")

aspirin = Ingredient("aspirin")

my_drug2.has_for_ingredient.append(aspirin)

print(my_drug2.has_for_ingredient)
print(aspirin.is_ingredient_of)#自动得到反向