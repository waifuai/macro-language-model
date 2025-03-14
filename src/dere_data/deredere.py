from .deredere_feeling import feeling_responses
from .deredere_family import family_responses
from .deredere_childhood import childhood_responses
from .deredere_insult import insult_responses
from .deredere_greeting import greeting_responses
from .deredere_question import question_responses
from .deredere_interest import interest_responses
from .deredere_farewell import farewell_responses

deredere_responses = {
    "feeling": feeling_responses,
    "family": family_responses,
    "childhood": childhood_responses,
    "insult": insult_responses,
    "greeting": greeting_responses,
    "question": question_responses,
    "interest": interest_responses,
    "farewell": farewell_responses,
}

deredere_default_responses = [
    "Hi!",
    "How are you?",
    "What's up?",
    "Let's have some fun!",
    "I'm so happy to see you!",
    "You're the best!",
    "I love spending time with you!",
    "You always make me smile!",
    "You're so amazing!",
    "I'm so lucky to have you in my life!"
]