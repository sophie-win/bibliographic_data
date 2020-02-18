from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo
)

from .nodeutils import NodeUtils


class Grouping(StructuredNode, NodeUtils):
    name = StringProperty()
    countries = RelationshipTo('.country.Country', 'MEMBER_OF')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                # 'countries': self.countries
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Country',
                'nodes_related': self.serialize_relationships(self.countries.all()),
            }
        ]
