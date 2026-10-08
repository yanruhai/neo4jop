from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, BooleanProperty, DateTimeProperty,
                      DateProperty, ArrayProperty, UniqueIdProperty, RelationshipTo, get_config, DoesNotExist)

from neomodel_exercise.model.models import Location, OntoClass,Person

config = get_config()
config.database_url = "bolt://neo4j:cloudtian101@localhost:7687"

try:
    persons=Person.nodes.all()
    node=OntoClass.nodes.get_or_none(name='graph1')
    for p in persons:
        if p.belongs_to.is_connected(node):
            rel=p.belongs_to.relationship(node)
            rel.name='BELONGS_TO'
            rel.save()
            print(f"已更新 {p.name} 的关系属性")





except DoesNotExist:
    print("数据库中没有找到对应的节点！")