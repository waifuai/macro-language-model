from .greetings import register_greeting_keywords
from .questions import register_question_keywords
from .family import register_family_keywords
from .feelings import register_feelings_keywords
from .interests import register_interests_keywords
from .general import register_general_keywords

__all__ = [
    "register_greeting_keywords",
    "register_question_keywords",
    "register_family_keywords",
    "register_feelings_keywords",
    "register_interests_keywords",
    "register_general_keywords"
]