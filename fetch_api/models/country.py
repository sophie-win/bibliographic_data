from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom
)

from .nodeutils import NodeUtils


class Country(StructuredNode):
    name = StringProperty()
    officialname = StringProperty()
    groupings = RelationshipFrom('.grouping.Grouping', 'MEMBER_OF')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                'officialname': self.officialname,
                'groupings': self.groupings
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Grouping',
                'nodes_related': self.serialize_relationships(self.groupings.all()),
            }
        ]


