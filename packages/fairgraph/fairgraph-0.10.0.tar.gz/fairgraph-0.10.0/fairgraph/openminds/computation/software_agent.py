"""
Structured information about a piece of software or web service that can perform a task autonomously.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class SoftwareAgent(KGObject):
    """
    Structured information about a piece of software or web service that can perform a task autonomously.
    """

    default_space = "computation"
    type_ = ["https://openminds.ebrains.eu/computation/SoftwareAgent"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the software agent.",
        ),
        Field("environment", "openminds.computation.Environment", "vocab:environment", doc="no description available"),
        Field(
            "software",
            "openminds.core.SoftwareVersion",
            "vocab:software",
            required=True,
            doc="no description available",
        ),
    ]
    existence_query_fields = ("name", "software")

    def __init__(self, name=None, environment=None, software=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, name=name, environment=environment, software=software
        )
