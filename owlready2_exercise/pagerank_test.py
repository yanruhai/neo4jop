from owlready2 import *

onto = get_ontology("http://example.org/domain_ontology.owl")

with onto:
    class Entity(Thing): pass

    class Arc(Thing):
        pass
    class ArcRelationshipFrom(ObjectProperty):
        domain=[Entity]
        range=[Arc]

    class ArcRelationshipTo(ObjectProperty):
        domain=[Arc]
        range=[Entity]

    class ArcVector(DataProperty):
        pass


def create_node(from_node,to_node):
    arc=Arc(from_node.name+"_"+to_node.name)
    from_node.ArcRelationshipFrom.append(arc)
    arc.ArcRelationshipTo.append(to_node)
    return arc


moonvalley=Entity('MoonValley')
piedrasrojas=Entity('piedrasrojas')
losflamencos=Entity('losflamencos')
arica=Entity('arica')
sanpedro=Entity('sanpedro')
calama=Entity('calama')
mp_arc=create_node(moonvalley,piedrasrojas)
pl_arc=create_node(piedrasrojas,losflamencos)
ls_arc=create_node(losflamencos,sanpedro)
sl_arc = create_node(sanpedro,losflamencos)
sa_arc=create_node(sanpedro,arica)
sc_arc=create_node(sanpedro,calama)
cs_arc=create_node(calama,sanpedro)
sm_arc=create_node(sanpedro,moonvalley)
as_arc=create_node(arica,sanpedro)

all_entities=list(onto.search(type=onto.Entity))
mp_arc.ArcVector=[1/len(all_entities),1/len(all_entities)]
print(mp_arc.ArcVector)
