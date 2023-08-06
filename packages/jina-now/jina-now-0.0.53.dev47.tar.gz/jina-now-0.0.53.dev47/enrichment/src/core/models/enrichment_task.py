from dataclasses import dataclass
from typing import List, Union

from enrichment.src.core.models.enrichments import EnrichmentTypes
from enrichment.src.core.models.modalities import Modalities
from enrichment.src.core.prompts import (
    generate_query_suggestions,
    generate_synonyms,
    generate_text_description,
)


@dataclass
class Attribute:
    name: str
    possible_values: None | List[str]
    exclusions: Union[None | str | int | float | List[Union[str | int | float]]] = None


@dataclass
class EnrichmentField:
    name: str
    modality: Modalities
    enrichment_type: EnrichmentTypes
    value: Union[None | str | int | float | List[Union[str | int | float]]] = None
    exclusions: Union[None | str | int | float | List[Union[str | int | float]]] = None

    def prompt(self, task_idx: int, enrichment_context: str = 'product') -> str:
        if self.enrichment_type == EnrichmentTypes.SYNONYMS:
            return generate_synonyms(
                task_idx=task_idx,
                attribute_name=self.name,
                possible_values=self.value,
                exclusions=self.exclusions,
            )
        elif self.enrichment_type == EnrichmentTypes.TEXT_DESCRIPTION:
            return generate_text_description(
                task_idx=task_idx, enrichment_context=enrichment_context
            )
        elif self.enrichment_type == EnrichmentTypes.QUERY_SUGGESTIONS:
            return generate_query_suggestions(
                task_idx=task_idx, enrichment_context=enrichment_context
            )


@dataclass
class EnrichmentTask:
    enrichment_context: str
    attributes: List[Attribute]
    enrichment_fields: List[EnrichmentField]

    def format_attributes_for_prompt(self) -> None | str:
        if self.attributes:
            attributes_str = f'These are some of the attributes that describe the {self.enrichment_context}.'
            attributes_str += ','.join(
                [attribute.name for attribute in self.attributes]
            )
            attributes_str += '\n'

            return attributes_str

        return None

    def format_attributes_and_values_for_prompt(self) -> None | str:
        if self.attributes:
            attributes_str = f'These are some of the attributes with possible values that describe the {self.enrichment_context}.'
            for attribute in self.attributes:
                attributes_str += (
                    '\n'
                    + f'''{attribute.name}: {';'.join(attribute.possible_values)}'''
                )

            return attributes_str

        return None
