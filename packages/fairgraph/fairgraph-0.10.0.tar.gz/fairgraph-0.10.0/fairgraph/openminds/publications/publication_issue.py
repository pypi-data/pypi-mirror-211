"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class PublicationIssue(KGObject):
    """ """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/PublicationIssue"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "is_part_of",
            "openminds.publications.PublicationVolume",
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Field("issue_number", str, "vocab:issueNumber", required=True, doc="no description available"),
    ]
    existence_query_fields = ("is_part_of", "issue_number")

    def __init__(self, is_part_of=None, issue_number=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, is_part_of=is_part_of, issue_number=issue_number
        )
