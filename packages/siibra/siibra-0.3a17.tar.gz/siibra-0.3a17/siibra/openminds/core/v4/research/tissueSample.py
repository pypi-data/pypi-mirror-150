# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/core/v4/research/tissueSample.schema.json

from typing import Any, Dict, List, Optional

from pydantic import Field
from siibra.openminds.base import SiibraBaseModel


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    anatomical_location: Optional[List[Any]] = Field(
        None,
        alias='anatomicalLocation',
        min_items=1,
        title='anatomicalLocation',
    )
    biological_sex: Optional[Dict[str, Any]] = Field(
        None,
        alias='biologicalSex',
        description='Differentiation of individuals of most species (animals and plants) based on the type of gametes they produce.',
        title='biologicalSex',
    )
    internal_identifier: Optional[str] = Field(
        None,
        alias='internalIdentifier',
        description='Term or code that identifies someone or something within a particular product.',
        title='internalIdentifier',
    )
    is_part_of: Optional[List[Any]] = Field(
        None,
        alias='isPartOf',
        description='Reference to the ensemble of multiple things or beings.',
        min_items=1,
        title='isPartOf',
    )
    laterality: Optional[List[Any]] = Field(
        None,
        alias='laterality',
        description='Differentiation between a pair of lateral homologous parts of the body.',
        max_items=2,
        min_items=1,
        title='laterality',
    )
    lookup_label: Optional[str] = Field(
        None,
        alias='lookupLabel',
        title='lookupLabel',
    )
    origin: Dict[str, Any] = Field(
        ...,
        alias='origin',
        description='Source at which something begins or rises, or from which something derives.',
        title='origin',
    )
    species: Dict[str, Any] = Field(
        ...,
        alias='species',
        description='Category of biological classification comprising related organisms or populations potentially capable of interbreeding, and being designated by a binomial that consists of the name of a genus followed by a Latin or latinized uncapitalized noun or adjective.',
        title='species',
    )
    studied_state: List[Any] = Field(
        ...,
        alias='studiedState',
        description='Reference to a point in time at which something or someone was studied in a particular mode or condition.',
        min_items=1,
        title='studiedState',
    )
    type_1: Dict[str, Any] = Field(
        ...,
        alias='type',
        description='Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.',
        title='type',
    )
