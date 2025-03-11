import random
from typing import List, Optional, Set

def maybe_use_small_talk(small_talk: List[str], used_small_talk: Set[str]) -> Optional[str]:
    """Uses small talk based on randomness"""
    unused_small_talk = [phrase for phrase in small_talk if phrase not in used_small_talk]
    if (random.random() < 0.1 and unused_small_talk):
        response = random.choice(unused_small_talk)
        used_small_talk.add(response)
        return response
    elif (random.random() < 0.1):
        # if all small talk has been used, we clear the used_small_talk
        # and pick a response again.
        used_small_talk.clear()
        response = random.choice(small_talk)
        used_small_talk.add(response)
        return random.choice(small_talk)
    return None