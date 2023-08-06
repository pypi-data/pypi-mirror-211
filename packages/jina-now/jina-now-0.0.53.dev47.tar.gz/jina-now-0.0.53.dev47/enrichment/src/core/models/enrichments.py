from enum import Enum


class EnrichmentTypes(Enum):
    SYNONYMS = 'synonyms'
    TEXT_DESCRIPTION = 'text_description'
    QUERY_SUGGESTIONS = 'query_suggestions'
