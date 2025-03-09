from typing import List, Tuple, Set

class ConversationContext:
    def __init__(self):
        self.conversation_history: List[Tuple[str, str]] = []
        self.used_responses: Set[str] = set()