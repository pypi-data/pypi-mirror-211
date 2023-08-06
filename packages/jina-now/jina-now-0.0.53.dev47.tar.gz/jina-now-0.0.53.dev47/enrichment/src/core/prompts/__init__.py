import inspect
from typing import List, Union


def system_description(
    enrichment_context: str = 'product',
    provided_attribute_with_values: None | str = None,
) -> str:
    context_expansion = provided_attribute_with_values or ''
    return f'''You are a helpful and terse assistant. Consider the following description enclosed in backticks.
        ```
        {enrichment_context}
        {context_expansion}
        ```
        BM25 is a ranking function used by search engines to estimate the relevance of documents to a given search query.
        The following tasks must be optimized for a search engine using the BM25 similarity method.'''


def generate_synonyms(
    task_idx: int,
    attribute_name: str,
    possible_values: [None | str | int | float | List[Union[str | int | float]]] = None,
    exclusions: Union[None | str | int | float | List[Union[str | int | float]]] = None,
    n_values: int = 5,
) -> str:
    possible_values_prompt = ''
    if possible_values:
        possible_values_prompt = inspect.cleandoc(
            f'''\
        which is currently characterized by the following values surrounded by backticks: ```{','.join(possible_values)}```.'''
        )

    exclusions_prompt = ''
    if exclusions:
        if type(exclusions) == list:
            exclusions_prompt = f'''Don't include the following keywords surrounded by backticks: ```{','.join(exclusions)}```.'''
        else:
            exclusions_prompt = (
                f'''Don't include the following keywords: {exclusions}.'''
            )

    final_prompt = ' '.join(
        [
            f'{task_idx}. Generate a comma separated list of synonyms for the {attribute_name} {possible_values_prompt}.',
            f'Generate a maximum of {n_values} values. {exclusions_prompt}',
        ]
    )
    return final_prompt


def generate_text_description(
    task_idx: int, enrichment_context: str = 'product'
) -> str:
    final_prompt = ' '.join(
        [
            f'{task_idx}. Generate a full text description of the {enrichment_context} taking into account the mentioned {enrichment_context} and attributes.',
            'The description must contain maximum of 50 words.',
        ]
    )
    return final_prompt


def generate_query_suggestions(
    task_idx: int, enrichment_context: str = 'product'
) -> str:
    final_prompt = ' '.join(
        [
            f'{task_idx}. Generate a comma separated list of possible search query patterns for finding the',
            f'{enrichment_context} using a search engine.',
        ]
    )
    return final_prompt
