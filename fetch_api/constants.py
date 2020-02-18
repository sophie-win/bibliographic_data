from neomodel import db

# countries = db.cypher_query(
#     '''
#     MATCH (n: Country)
#     WHERE NOT n.name CONTAINS ';'
#     RETURN DISTINCT n.name AS countries
#     '''
# )[0]

countries = db.cypher_query('''
    match (n) 
    with n, [x in keys(n) WHERE n[x]=~'Ca.*'] as doesMatch
    where size(doesMatch) > 0
    return n as countries
    ''')[0]
# COUNTRIES = sorted([country[0] for country in countries])

search_data = db.cypher_query('''
    match (n) 
    with n, [x in keys(n) WHERE n[x]=~'Jo.*'] as doesMatch
    where size(doesMatch) > 0
    return n
    ''')[0]
