import random

def get_current_dere(affection):
    if affection < -5:
        return "tsundere"
    elif -5 <= affection <= 0:
        return "yandere"
    elif 1 <= affection <= 40:
        return "kuudere"
    elif 41 <= affection <= 75:
        return "dandere"
    else:
        return "deredere"

def maybe_change_dere(waifu_memory, current_dere, dere_types, used_responses, debug, *responses):
    """Randomly changes the dere type and returns a dere-specific response."""
    if debug:
        print(f"Type of used_responses in maybe_change_dere: {type(used_responses)}")
    if random.randint(0, 9) == 0:
        current_dere = random.choice(dere_types)
        response = dere_response(waifu_memory, current_dere, used_responses, debug, *responses)
        if debug:
            print(f"{waifu_memory.name}: (I feel a little different...)")
            print()
        used_responses.add(response)
        return response
    return dere_response(waifu_memory, current_dere, used_responses, debug, *responses)

def dere_response(waifu_memory, current_dere, used_responses, debug, *responses):
    """Returns a response based on the current dere type."""
    if debug:
        print(f"Type of used_responses in dere_response: {type(used_responses)}")
    if not responses:
        if current_dere == "tsundere":
            responses = ("B-baka! It's not like I care what you say!", "Hmph! Whatever.")
        elif current_dere == "yandere":
            responses = ("You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone.")
        elif current_dere == "kuudere":
            responses = ("Hmph.", "...", "Is that so.", "I see.", "Understood.")
        elif current_dere == "dandere":
            responses = ("U-um...", "O-okay...", "I-I understand...", "If you say so...", "S-sure...")
        elif current_dere == "himedere":
            responses = ("Bow down to me, you peasant!", "You are lucky to be in my presence.", "Hmph, how amusing.", "Do as I command!", "You should be honored.")

    unused_responses = [r for r in responses if r not in used_responses]

 # Ensure responses is always a tuple
    if not unused_responses:
        used_responses.clear()
        unused_responses = list(responses)

    chosen_response = random.choice(unused_responses)
    used_responses.add(chosen_response)
    return chosen_response