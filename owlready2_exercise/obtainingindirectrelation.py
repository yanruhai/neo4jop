from owlready2 import *

onto = get_ontology("http://example.org/test.owl")

with onto:
    class BodyPart(Thing): pass
    class part_of(BodyPart >> BodyPart, TransitiveProperty): pass
    abdomen          = BodyPart("abdomen")
    heart            = BodyPart("heart"           , part_of = [abdomen])
    left_ventricular = BodyPart("left_ventricular", part_of = [heart])
    kidney           = BodyPart("kidney"          , part_of = [abdomen])

print(left_ventricular.part_of)


print(left_ventricular.INDIRECT_part_of)
