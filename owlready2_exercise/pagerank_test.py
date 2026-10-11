from owlready2 import *

onto = get_ontology("http://example.org/domain_ontology.owl")

d=0.85 #全局阻抗

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

    class NodeVector(DataProperty):
        pass


def create_node(from_node,to_node):
    arc=Arc(from_node.name+"_"+to_node.name)
    from_node.ArcRelationshipFrom.append(arc)
    arc.ArcRelationshipTo.append(to_node)
    return arc

def init_node_vector(node,num_nodes):
    node.NodeVector = [1 / num_nodes, len(node.ArcRelationshipFrom), num_nodes]
    #vector is 1/|V|,|E'(u)|,|V|

def Msg(node):
    vector1=d*node.NodeVector[0]/node.NodeVector[1]
    for arcNode in node.ArcRelationshipFrom:
        arcNode.ArcVector=[vector1]

def Agg(node):
    v_list = default_world.search(ArcRelationshipTo=node)
    nv=0
    for v in v_list:
        nv+=v.ArcVector[0]
    nv+=(1-d)/node.NodeVector[2]#最后加上1-d/|V|
    node.NodeVector[0]=nv

def print_nodes(all_entities):
    sum=0
    for entity in all_entities:
        sum+=entity.NodeVector[0]
        print(entity.name+":"+str(entity.NodeVector[0])+"\n")
    print('最终结果:'+str(sum))



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
for entity in all_entities:
    init_node_vector(entity,len(all_entities))
count=0
while count<50:
    for entity in all_entities:
        Msg(entity)
    for entity in all_entities:
        Agg(entity)
    count+=1


print_nodes(all_entities)

