import copy

import tiktoken
from enrichment.src.core.models.enrichment_task import EnrichmentTask
from enrichment.src.core.models.enrichments import EnrichmentTypes
from enrichment.src.core.prompts import system_description

from core.models.model_generation_config import (
    MODEL_MAX_TOKENS,
    MODEL_NAME,
    product_description_generation_settings,
    query_suggestions_generation_settings,
    synonyms_generation_settings,
)
from core.models.plan import Plan, Step


def _estimated_output_tokens(enrichment_type: EnrichmentTypes) -> int:
    if enrichment_type == EnrichmentTypes.SYNONYMS:
        return synonyms_generation_settings.max_tokens
    elif enrichment_type == EnrichmentTypes.TEXT_DESCRIPTION:
        return product_description_generation_settings.max_tokens
    elif enrichment_type == EnrichmentTypes.QUERY_SUGGESTIONS:
        return query_suggestions_generation_settings.max_tokens


def create_plan(
    enrichment_task: EnrichmentTask, max_context_length: int = MODEL_MAX_TOKENS
) -> Plan:
    if not len(enrichment_task.enrichment_fields):
        raise RuntimeError('There are no enrichment fields in the enrichment task.')

    plan = Plan()
    system_prompt = system_description(
        enrichment_context=enrichment_task.enrichment_context,
        provided_attribute_with_values=enrichment_task.format_attributes_and_values_for_prompt(),
    )
    system_prompt_num_tokens = len(
        tiktoken.encoding_for_model(MODEL_NAME).encode(system_prompt)
    )

    # reduce system description
    if system_prompt_num_tokens > max_context_length:
        system_prompt = system_description(
            enrichment_context=enrichment_task.enrichment_context,
            provided_attribute_with_values=enrichment_task.format_attributes_for_prompt(),
        )
        system_prompt_num_tokens = len(
            tiktoken.encoding_for_model(MODEL_NAME).encode(system_prompt)
        )

    # check if reduction helped
    if system_prompt_num_tokens > max_context_length:
        raise RuntimeError(
            'System description exceeds max context length even after reduction!'
        )

    current_prompt = copy.copy(system_prompt)
    current_prompt_num_tokens = copy.copy(system_prompt_num_tokens)
    current_estimated_output_tokens = 0

    for idx, enrichment_field in enumerate(enrichment_task.enrichment_fields, start=1):
        new_prompt = enrichment_field.prompt(
            task_idx=idx, enrichment_context=enrichment_task.enrichment_context
        )
        new_prompt_tokens = len(
            tiktoken.encoding_for_model(MODEL_NAME).encode(new_prompt)
        )
        new_prompt_output_tokens = _estimated_output_tokens(
            enrichment_field.enrichment_type
        )

        estimated_total_tokens = (
            current_prompt_num_tokens
            + current_estimated_output_tokens
            + new_prompt_tokens
            + new_prompt_output_tokens
        )
        if estimated_total_tokens > MODEL_MAX_TOKENS:
            step = Step(
                prompt=current_prompt,
                input_tokens=current_prompt_num_tokens,
                estimated_output_tokens=current_estimated_output_tokens,
            )
            plan.add_step(step)
            current_prompt = system_prompt + '\n' + new_prompt
            current_prompt_num_tokens = system_prompt_num_tokens + new_prompt_tokens
            current_estimated_output_tokens = new_prompt_output_tokens
        else:
            current_prompt += '\n' + new_prompt
            current_prompt_num_tokens += new_prompt_tokens
            current_estimated_output_tokens += new_prompt_output_tokens

    step = Step(
        prompt=current_prompt,
        input_tokens=current_prompt_num_tokens,
        estimated_output_tokens=current_estimated_output_tokens,
    )
    plan.add_step(step)
    return plan
