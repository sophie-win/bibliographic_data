from .constants import countries
from .models import (Country)
from neomodel import db

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Country': Country,
}


def fetch_nodes(fetch_info):
    node_type = fetch_info['node_type']
    search_word = fetch_info['name']
    limit = fetch_info['limit']
    start = ((fetch_info['page'] - 1) * limit)
    end = start + limit
    node_set = filter_nodes(MODEL_ENTITIES[node_type], search_word)
    fetched_nodes = node_set[start:end]

    return [node.serialize for node in fetched_nodes]


def filter_nodes(node_type, search_text):
    node_set = node_type.nodes

    # On Address nodes we want to check the search_text against the address property
    # For any other we check against the name property
    print("node type" + node_type.__name__)
    if node_type.__name__ == 'Country':
        node_set.filter(address__icontains=search_text)
    else:
        node_set.filter(name__icontains=search_text)
        print("real filter " + node_set)

    # Only entities store jurisdiction info
    # if node_type.__name__ == 'Entity':
    #     node_set.filter(jurisdiction__icontains=jurisdiction)
    #
    # node_set.filter(countries__icontains=country)
    # node_set.filter(sourceID__icontains=source_id)

    return node_set


def fetch_countries():
    # print(countries)
    # print(countries[0])
    for node in countries[0]:

        print(node)
        if isinstance(node, int):
            print("here")
        else:
            node_properties = _get_node_properties(node)
            for keyValue in node_properties:
                print(node_properties[keyValue])
                print("Ca" in node_properties[keyValue])
            print(node_properties.keys())

            # print(node.labels)
            # for x in node.labels:
            #     print(x)

    return countries


def get_suggested_nodes(a):
    query2 = f'''
    match (n) 
    with n, [x in keys(n) WHERE n[x]=~'(?i){a}.*' and NOT n:Person] as doesMatch
    where size(doesMatch) > 0
    return n + doesMatch as countries limit 10
    '''
    results = {}
    # print(query2)
    results = db.cypher_query(query2)[0]

    # print(countries)
    #
    # for node in countries[0]:
    #
    #     if isinstance(node, int):
    #         print("here")
    #     else:
    #         node_properties = _get_node_properties(node)
    #         for keyValue in node_properties:
    #             print(node_properties[keyValue])
    #             print("Ca" in node_properties[keyValue])
    #         print(node_properties.keys())

    # print(node.labels)
    # for x in node.labels:
    #     print(x)

    return results


def book_and_author(a):
    query = f'''match (a:Book)-[r]-(b:Author) where a.title = '{a}' return a, b'''

    results = {}
    results = db.cypher_query(query)[0]
    return results


def sample_data():
    a = '{maxLevel:2}'
    b = '{.*, label:labels(node)[0]}'
    c = ' {.*, fromNode:{label:'
    d = '}, toNode:{label:labels(endNode(rel))[0], id:endNode(rel).id}}'
    e = '{nodes:nodes, relationships:rels}'
    query = f'''match (a:Publisherhey)-[rs]-(b:Journal) where a.name = 'Publisher'
 CALL apoc.path.subgraphAll(a, {a}) YIELD nodes, relationships
    WITH [node in nodes | node {b}] as nodes, 
    [rel in relationships | rel {c}labels(startNode(rel))[0], id:startNode(rel).id {d}] as rels
    WITH {e} as json
    RETURN apoc.convert.toJson(json)
    '''

    results = {}
    # print(query)
    results = db.cypher_query(query)[0]
    return results


def json_api_call(q_data):
    s1 = '{maxLevel:2, limit:30}'
    s2 = '{.*, id:node.id,labels:[labels(node)[0]]}'
    s3 = '{ .*,type: type(rel), startNode:startNode(rel).id , endNode:endNode(rel).id, id: ID(rel)}'
    s4 = '{nodes:nodes, relationships:rels}'
    query_str = f'''
            MATCH (n) 
            WHERE n.name = '{q_data}' and NOT n:Person
            CALL apoc.path.subgraphAll(n, {s1}) YIELD nodes, relationships
            WITH [node in nodes | node {s2}] as nodes, 
            [rel in relationships | rel  
            {s3}] as rels
            WITH {s4} as json
            RETURN apoc.convert.toJson(json)
            '''
    # print(query_str)
    # results = {}
    results = db.cypher_query(query_str)[0]
    # print(results)
    return results


def get_first_generation_family_tree():
    first_gen = '1'
    query = f'''Match (n:Person) where n.generation = '{first_gen}' return n.name, ID(n)'''
    results = db.cypher_query(query)[0]
    # print(query)
    return results


def get_nodes_and_relationships(node_id):
    s1 = '{maxLevel:1, limit:30}'
    s2 = '{.*, id:node.id,labels:[labels(node)[0]]}'
    s3 = '{ .*,type: type(rel), startNode:startNode(rel).id , endNode:endNode(rel).id, id: ID(rel)}'
    s4 = '{nodes:nodes, relationships:rels}'
    query_str = f'''
            MATCH (n) 
            WHERE n.id = {node_id} and NOT n:Person
            CALL apoc.path.subgraphAll(n, {s1}) YIELD nodes, relationships
            WITH [node in nodes | node {s2}] as nodes, 
            [rel in relationships | rel  
            {s3}] as rels
            WITH {s4} as json
            RETURN apoc.convert.toJson(json)
            '''
    # print(query_str)
    # results = {}
    results = db.cypher_query(query_str)[0]
    # print(results)
    return results


def family_tree_json_api_call(q_data):
    s1 = '{maxLevel:2}'
    s2 = '{.*, id:node.id,labels:[labels(node)[0]]}'
    s3 = '{ .*,type: type(rel), startNode:startNode(rel).id , endNode:endNode(rel).id}'
    s4 = '{nodes:nodes, relationships:rels}'
    query = f'''MATCH (n:Person) 
                WHERE n.name = '{q_data}'
                CALL apoc.path.subgraphAll(n, {s1}) YIELD nodes, relationships
                WITH [node in nodes | node {s2}] as nodes
                , 
                [rel in relationships | rel  
                {s3}] as rels
                WITH {s4} as json
                RETURN apoc.convert.toJson(json)'''
    # print(query)
    # results = {}
    results = db.cypher_query(query)[0]
    # print(results)
    return results


def family_tree_normal(q_data):
    query = f'''MATCH (n:Person)-[rs]->(m:Person)
                WHERE n.name = '{q_data}' and type(rs)='Mother_Of' 
                return n,type(rs),m union all
                MATCH (n:Person)-[rs]->(m:Person)
                WHERE n.name = '{q_data}' and type(rs)='Father_Of' 
                return n,type(rs),m union all 
                MATCH (n:Person)-[rs]-(m:Person)
 WHERE n.name = '{q_data}' and type(rs)='Married' 
 return n,type(rs),m'''
    results = db.cypher_query(query)[0]

    # if q_data == 'Mary Anne Wedgwood':
    #      print(query)
    #      print(results)
    return results


def family_tree_child(q_data):
    query = f'''MATCH (n:Person)-[rs]-(m:Person)
                WHERE ID(n) = {q_data} and type(rs)='Father_Of'  
                return n,type(rs),m union all
                MATCH (n:Person)-[rs]-(m:Person)
                WHERE ID(n) = {q_data} and type(rs)='Mother_Of'  
                return n,type(rs),m'''
    # print(len('Charlotte Mildred Massing'))
    results = db.cypher_query(query)[0]
    return results


def _get_node_properties(node):
    """Get the properties from a neo4j.v1.types.graph.Node object."""
    # 1.6.x and newer have it as `_properties`
    if hasattr(node, '_properties'):
        return node._properties
    # 1.5.x and older have it as `properties`
    else:
        return node.properties
