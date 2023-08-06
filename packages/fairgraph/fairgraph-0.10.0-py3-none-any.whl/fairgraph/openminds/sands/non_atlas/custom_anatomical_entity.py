"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class CustomAnatomicalEntity(KGObject):
    """ """

    default_space = "spatial"
    type_ = ["https://openminds.ebrains.eu/sands/CustomAnatomicalEntity"]
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
            doc="Word or phrase that constitutes the distinctive designation of the custom anatomical entity.",
        ),
        Field(
            "has_annotations",
            "openminds.sands.CustomAnnotation",
            "vocab:hasAnnotation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "related_uberon_term",
            ["openminds.controlledterms.Organ", "openminds.controlledterms.UBERONParcellation"],
            "vocab:relatedUBERONTerm",
            doc="no description available",
        ),
        Field(
            "relation_assessments",
            ["openminds.sands.QualitativeRelationAssessment", "openminds.sands.QuantitativeRelationAssessment"],
            "vocab:relationAssessment",
            multiple=True,
            doc="no description available",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        has_annotations=None,
        related_uberon_term=None,
        relation_assessments=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            has_annotations=has_annotations,
            related_uberon_term=related_uberon_term,
            relation_assessments=relation_assessments,
        )
