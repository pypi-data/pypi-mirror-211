"""
An International Standard Book Number of the International ISBN Agency.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class ISBN(KGObject):
    """
    An International Standard Book Number of the International ISBN Agency.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/ISBN"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the ISBN."),
    ]
    existence_query_fields = ("identifier",)

    def __init__(self, identifier=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, space=space, scope=scope, data=data, identifier=identifier)
