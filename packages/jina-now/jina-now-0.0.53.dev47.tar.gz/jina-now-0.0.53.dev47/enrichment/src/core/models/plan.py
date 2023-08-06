from dataclasses import dataclass
from typing import List


@dataclass
class Step:
    prompt: str
    input_tokens: int
    estimated_output_tokens: int

    def prompt_as_lines(self) -> List[str]:
        return self.prompt.split('\n')


class Plan:
    def __init__(self):
        self._steps: List[Step] = []
        self._total_input_tokens: int = 0
        self._total_estimated_output_tokens: int = 0

    def add_step(self, step: Step):
        self._steps.append(step)
        self._total_input_tokens += step.input_tokens
        self._total_estimated_output_tokens += step.estimated_output_tokens

    @property
    def steps(self) -> List[Step]:
        return self._steps

    @property
    def total_input_tokens(self) -> int:
        return self._total_input_tokens

    @property
    def total_estimated_output_tokens(self) -> int:
        return self._total_estimated_output_tokens
