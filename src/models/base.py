from abc import ABC, abstractmethod

class BaseSummarizer(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        """Summarize the input text."""
        pass

class BaseTopicsResolver(ABC):
    @abstractmethod
    def resolve_topics(self, text: str) -> list:
        """Extract topics from the input text."""
        pass
