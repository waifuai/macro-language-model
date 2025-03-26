from typing import Dict, List, Tuple, Any, Optional

class Registry:
    def __init__(self):
        # self.keywords: Dict[str, List[Tuple[str, Any]]] = {} # REMOVED
        self.transformations: Dict[str, Tuple[Any, Optional[str], int]] = {}

    # REMOVED defkeyword
    # def defkeyword(self, keyword: str, responses: List[str]) -> None:
    #     """Defines a keyword and its associated responses."""
    #     if responses and isinstance(responses[0], tuple):
    #         self.keywords[keyword] = responses
    #     else:
    #         self.keywords[keyword] = [(keyword, response) for response in responses]

    # REMOVED defsynonym
    # def defsynonym(self, word: str, *synonyms: str) -> None:
    #     """Defines synonyms for a given word."""
    #     if word not in self.keywords:
    #         return
    #
    #     for syn in synonyms:
    #         self.keywords[syn] = self.keywords[word][:]  # Create a copy of list.

    # REMOVED def_topic_response
    # def def_topic_response(self, topic: str, pattern: str, response: str) -> None:
    #     """Defines a response for a specific topic."""
    #     if topic not in self.keywords:
    #         self.keywords[topic] = []
    #     self.keywords[topic].append((pattern, response))