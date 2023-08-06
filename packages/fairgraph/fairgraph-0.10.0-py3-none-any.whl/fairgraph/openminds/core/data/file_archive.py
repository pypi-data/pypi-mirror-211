"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class FileArchive(KGObject):
    """ """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/FileArchive"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Field(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            required=True,
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Field(
            "source_datas", "openminds.core.File", "vocab:sourceData", multiple=True, doc="no description available"
        ),
    ]
    existence_query_fields = ("iri", "format")

    def __init__(self, iri=None, format=None, source_datas=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, iri=iri, format=format, source_datas=source_datas
        )
