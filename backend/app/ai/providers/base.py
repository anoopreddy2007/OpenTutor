from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract interface for language-model providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response from the language model."""
        raise NotImplementedError