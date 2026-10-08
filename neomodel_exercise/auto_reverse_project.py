from pathlib import Path

from neo4j import GraphDatabase

# 1. Neo4j 类型到 neomodel 属性的映射映射表
TYPE_MAP = {
    'String': 'StringProperty',
    'Long': 'IntegerProperty',
    'Integer': 'IntegerProperty',
    'Float': 'FloatProperty',
    'Boolean': 'BooleanProperty',
    'Date': 'DateProperty',
    'DateTime': 'DateTimeProperty',
    'ZonedDateTime': 'DateTimeProperty',
    'StringArray': 'ArrayProperty(StringProperty())',
}


def generate_neomodel_models(uri, auth):
    driver = GraphDatabase.driver(uri, auth=auth)

    with driver.session() as session:
        # 查询所有 Node 属性定义
        result = session.run("""
            CALL db.schema.nodeTypeProperties()
            YIELD nodeType, propertyName, propertyTypes
            RETURN nodeType, propertyName, propertyTypes
        """)

        nodes_schema = {}
        for record in result:
            # 清理 Label 格式 (例如把 `Person` 提取出来)
            raw_label = record["nodeType"]
            label = raw_label.replace(":`", "").replace("`", "").replace(":", "")

            prop_name = record["propertyName"]
            prop_type = record["propertyTypes"][0] if record["propertyTypes"] else 'String'

            if label not in nodes_schema:
                nodes_schema[label] = {}
            nodes_schema[label][prop_name] = TYPE_MAP.get(prop_type, 'StringProperty')

    # 生成代码文本
    lines = [
        "from neomodel import (StructuredNode, StringProperty, IntegerProperty, ",
        "                      FloatProperty, BooleanProperty, DateTimeProperty, ",
        "                      DateProperty, ArrayProperty, UniqueIdProperty)\n"
    ]

    for label, props in nodes_schema.items():
        lines.append(f"class {label}(StructuredNode):")
        for prop_name, prop_type in props.items():
            # 自动把 uuid 或 uid 识别为主键，其余为普通属性
            if prop_name.lower() in ['uid', 'uuid', 'id']:
                lines.append(f"    {prop_name} = UniqueIdProperty()")
            else:
                lines.append(f"    {prop_name} = {prop_type}()")
        lines.append("\n")

    return "\n".join(lines)

# --- 使用示例 ---
code = generate_neomodel_models("bolt://localhost:7687", ("neo4j", "cloudtian101"))
output_path = Path("model/models.py")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(code, encoding="utf-8")
print(f"成功导出 neomodel 模型至: {output_path.resolve()}")