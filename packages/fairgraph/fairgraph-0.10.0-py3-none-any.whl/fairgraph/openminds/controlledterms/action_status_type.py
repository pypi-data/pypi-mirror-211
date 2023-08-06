"""
Structured information about the status of an action.
    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `active <https://schema.org/ActiveActionStatus>`_
         - An in-progress action.
       * - `completed <https://schema.org/CompletedActionStatus>`_
         - An action that has already taken place with a successful outcome.
       * - inactive
         - A pending or suspended action.
       * - `failed <https://schema.org/FailedActionStatus>`_
         - An action that failed to complete or completed but produced an error.
       * - paused
         - A temporarily stopped action that can be resumed at a later point in time.
       * - `potential <https://schema.org/PotentialActionStatus>`_
         - A description of an action that is supported.
       * - pending
         - An action which is awaiting execution.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class ActionStatusType(KGObject):
    """
    Structured information about the status of an action.
    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `active <https://schema.org/ActiveActionStatus>`_
         - An in-progress action.
       * - `completed <https://schema.org/CompletedActionStatus>`_
         - An action that has already taken place with a successful outcome.
       * - inactive
         - A pending or suspended action.
       * - `failed <https://schema.org/FailedActionStatus>`_
         - An action that failed to complete or completed but produced an error.
       * - paused
         - A temporarily stopped action that can be resumed at a later point in time.
       * - `potential <https://schema.org/PotentialActionStatus>`_
         - A description of an action that is supported.
       * - pending
         - An action which is awaiting execution.

    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/ActionStatusType"]
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
            doc="Word or phrase that constitutes the distinctive designation of the action status type.",
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
            doc="Longer statement or account giving the characteristics of the action status type.",
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
