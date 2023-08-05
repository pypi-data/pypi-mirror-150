# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/SANDS/v3/miscellaneous/quantitativeRelationAssessment.schema.json

from typing import Any, Dict, List, Optional, Union

from pydantic import Field
from siibra.openminds.base import SiibraBaseModel


class QuantitativeOverlapItem(SiibraBaseModel):
    type_of_uncertainty: Optional[Any] = Field(
        None,
        alias='typeOfUncertainty',
        description='Distinct technique used to quantify the uncertainty of a measurement.',
        title='typeOfUncertainty',
    )
    uncertainty: Optional[List[float]] = Field(
        None,
        description='Quantitative value range defining the uncertainty of a measurement.',
        max_items=2,
        min_items=2,
        title='uncertainty',
    )
    unit: Optional[Any] = Field(
        None,
        description='Determinate quantity adopted as a standard of measurement.',
        title='unit',
    )
    value: float = Field(..., description='Entry for a property.', title='value')


class QuantitativeOverlapItem1(SiibraBaseModel):
    max_value: float = Field(
        ...,
        alias='maxValue',
        description='Greatest quantity attained or allowed.',
        title='maxValue',
    )
    max_value_unit: Optional[Any] = Field(
        None, alias='maxValueUnit', title='maxValueUnit'
    )
    min_value: float = Field(
        ...,
        alias='minValue',
        description='Smallest quantity attained or allowed.',
        title='minValue',
    )
    min_value_unit: Optional[Any] = Field(
        None, alias='minValueUnit', title='minValueUnit'
    )


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    criteria: Optional[Dict[str, Any]] = Field(
        None,
        alias='criteria',
        description='Aspects or standards on which a judgement or decision is based.',
        title='criteria',
    )
    in_relation_to: Dict[str, Any] = Field(
        ...,
        alias='inRelationTo',
        description='Reference to a related element.',
        title='inRelationTo',
    )
    quantitative_overlap: Union[
        'QuantitativeOverlapItem', 'QuantitativeOverlapItem1'
    ] = Field(..., alias='quantitativeOverlap')
