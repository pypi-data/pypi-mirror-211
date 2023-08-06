from dataclasses import dataclass

MODEL_NAME = 'gpt-3.5-turbo'
MODEL_MAX_TOKENS = 2048
TASK_MAX_TOKENS = 400


@dataclass
class GPTGenerationSettings:
    max_tokens: int
    temperature: float
    top_p: int
    frequency_penalty: float
    presence_penalty: float

    def __post_init__(self):
        if self.max_tokens > TASK_MAX_TOKENS:
            raise ValueError(
                f'{self.__class__.__name__}.max_tokens cannot exceed the allowed per task max tokens of {TASK_MAX_TOKENS}.'
            )


synonyms_generation_settings = GPTGenerationSettings(
    max_tokens=60, temperature=0.4, top_p=1, frequency_penalty=1.0, presence_penalty=1.0
)

product_description_generation_settings = GPTGenerationSettings(
    max_tokens=50, temperature=0.4, top_p=1, frequency_penalty=0.5, presence_penalty=0.5
)

query_suggestions_generation_settings = GPTGenerationSettings(
    max_tokens=120,
    temperature=1.0,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.0,
)
