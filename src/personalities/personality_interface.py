from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set, Tuple

class PersonalityInterface(ABC):

    @abstractmethod
    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        """Generates a response to the user's input."""
        pass

    @abstractmethod
    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        """Introduces a new topic."""
        pass

    @abstractmethod
    def get_default_response(self, context: Dict[str, Any]) -> str:
        """Gets a default response."""
        pass

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """Gets personality-specific data."""
        pass

    @abstractmethod
    def maybe_introduce_topic(self, topic_manager: Any, input_str: str, turn_count: int) -> Optional[str]:
        """Potentially introduces a new topic."""
        pass

    @abstractmethod
    def respond_based_on_current_topic(self, topic_manager: Any, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], context: Dict[str, Any], response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]:
        """Responds based on the current topic."""
        pass

    @abstractmethod
    def handle_keywords(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], debug: bool) -> Optional[str]:
        """Handles general keywords."""
        pass