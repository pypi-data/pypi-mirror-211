"""

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - sweet substance
         - Any chemical compound that tastes sweet.
       * - salty substance
         - Any chemical compound that tastes salty.
       * - bitter substance
         - Any chemical compound that tastes bitter.
       * - sour substance
         - Any chemical compound that tastes sour.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class GustatoryStimulusType(KGObject):
    """

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - sweet substance
         - Any chemical compound that tastes sweet.
       * - salty substance
         - Any chemical compound that tastes salty.
       * - bitter substance
         - Any chemical compound that tastes bitter.
       * - sour substance
         - Any chemical compound that tastes sour.

    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/GustatoryStimulusType"]
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
            doc="Word or phrase that constitutes the distinctive designation of the gustatory stimulus type.",
        ),
        Field(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the gustatory stimulus type.",
        ),
        Field(
            "interlex_identifier",
            IRI,
            "vocab:interlexIdentifier",
            doc="Persistent identifier for a term registered in the InterLex project.",
        ),
        Field(
            "knowledge_space_link",
            IRI,
            "vocab:knowledgeSpaceLink",
            doc="Persistent link to an encyclopedia entry in the Knowledge Space project.",
        ),
        Field(
            "preferred_ontology_identifier",
            IRI,
            "vocab:preferredOntologyIdentifier",
            doc="Persistent identifier of a preferred ontological term.",
        ),
        Field(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        description=None,
        interlex_identifier=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
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
            definition=definition,
            description=description,
            interlex_identifier=interlex_identifier,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
        )
