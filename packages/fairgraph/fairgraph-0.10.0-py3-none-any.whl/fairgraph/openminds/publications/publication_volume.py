"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class PublicationVolume(KGObject):
    """ """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/PublicationVolume"]
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
            "openminds.publications.Periodical",
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Field("volume_number", str, "vocab:volumeNumber", required=True, doc="no description available"),
    ]
    existence_query_fields = ("is_part_of", "volume_number")

    def __init__(self, is_part_of=None, volume_number=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, is_part_of=is_part_of, volume_number=volume_number
        )
