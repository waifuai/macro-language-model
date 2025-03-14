import random
from typing import Optional, List
from dere_context import DereContext
from dere_data import dere_types

def maybe_change_dere(context: DereContext, dere_types: List[str]) -> Optional[str]:
    """Potentially changes the waifu's dere type based on affection and randomness."""
    if context.debug:
        print(f"maybe_change_dere called with context: {context}")
    if context.waifu_memory.affection > 80:
        if random.random() < 0.2:  # 20% chance to switch
            new_dere = random.choice(dere_types)
            if context.debug:
                print(f"Changing dere from {context.current_dere} to {new_dere}")
            context.current_dere = new_dere
            return f"Dere type changed to {new_dere}!"
    elif context.waifu_memory.affection < 20:
        if random.random() < 0.2:  # 20% chance to switch
            new_dere = random.choice(dere_types)
            if context.debug:
                print(f"Changing dere from {context.current_dere} to {new_dere}")
            context.current_dere = new_dere
            return f"Dere type changed to {new_dere}!"
    if context.debug:
        print(f"Dere unchanged. Affection: {context.waifu_memory.affection}")
    return None