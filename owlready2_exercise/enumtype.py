from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
  class MyEnum(Datatype):
    equivalent_to = [ OneOf(["Male", "Female", "Other"]) ]

with onto:
  class my_prop(DataProperty):
    range = [ MyEnum ]

print(onto.MyEnum())