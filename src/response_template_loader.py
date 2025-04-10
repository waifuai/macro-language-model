from typing import Dict, List
# Corrected imports:
from response_templates.tsundere import tsundere_responses
from response_templates.yandere import yandere_responses
from response_templates.kuudere import kuudere_responses
from response_templates.dandere import dandere_responses
from response_templates.himedere import himedere_responses
from response_templates.deredere import deredere_responses

def load_response_templates() -> Dict[tuple[str, str], List[str]]:
    """Loads and organizes response templates."""
    return {
        ("feeling", "tsundere"): tsundere_responses["feeling"],
        ("family", "tsundere"): tsundere_responses["family"],
        ("childhood", "tsundere"): tsundere_responses["childhood"],
        ("insult", "tsundere"): tsundere_responses["insult"],
        ("compliment", "tsundere"): tsundere_responses["compliment"],
        ("interest_manga", "tsundere"): tsundere_responses["interest_manga"],
        ("interest_anime", "tsundere"): tsundere_responses["interest_anime"],
        ("interest_games", "tsundere"): tsundere_responses["interest_games"],
        ("interest_cooking", "tsundere"): tsundere_responses["interest_cooking"],
        ("relationship_status", "tsundere"): tsundere_responses["relationship_status"],
        ("favorite_food", "tsundere"): tsundere_responses["favorite_food"],
        ("personality_quirks", "tsundere"): tsundere_responses["personality_quirks"],
        ("feeling", "yandere"): yandere_responses["feeling"],
        ("family", "yandere"): yandere_responses["family"],
        ("childhood", "yandere"): yandere_responses["childhood"],
        ("insult", "yandere"): yandere_responses["insult"],
        ("compliment", "yandere"): yandere_responses["compliment"],
        ("interest_manga", "yandere"): yandere_responses["interest_manga"],
        ("interest_anime", "yandere"): yandere_responses["interest_anime"],
        ("interest_games", "yandere"): yandere_responses["interest_games"],
        ("interest_cooking", "yandere"): yandere_responses["interest_cooking"],
        ("relationship_status", "yandere"): yandere_responses["relationship_status"],
        ("favorite_food", "yandere"): yandere_responses["favorite_food"],
        ("personality_quirks", "yandere"): yandere_responses["personality_quirks"],
        ("feeling", "kuudere"): kuudere_responses["feeling"],
        ("family", "kuudere"): kuudere_responses["family"],
        ("childhood", "kuudere"): kuudere_responses["childhood"],
        ("insult", "kuudere"): kuudere_responses["insult"],
        ("compliment", "kuudere"): kuudere_responses["compliment"],
        ("interest_manga", "kuudere"): kuudere_responses["interest_manga"],
        ("interest_anime", "kuudere"): kuudere_responses["interest_anime"],
        ("interest_games", "kuudere"): kuudere_responses["interest_games"],
        ("interest_cooking", "kuudere"): kuudere_responses["interest_cooking"],
        ("relationship_status", "kuudere"): kuudere_responses["relationship_status"],
        ("favorite_food", "kuudere"): kuudere_responses["favorite_food"],
        ("personality_quirks", "kuudere"): kuudere_responses["personality_quirks"],
        ("feeling", "dandere"): dandere_responses["feeling"],
        ("family", "dandere"): dandere_responses["family"],
        ("childhood", "dandere"): dandere_responses["childhood"],
        ("insult", "dandere"): dandere_responses["insult"],
        ("compliment", "dandere"): dandere_responses["compliment"],
        ("interest_manga", "dandere"): dandere_responses["interest_manga"],
        ("interest_anime", "dandere"): dandere_responses["interest_anime"],
        ("interest_games", "dandere"): dandere_responses["interest_games"],
        ("interest_cooking", "dandere"): dandere_responses["interest_cooking"],
        ("relationship_status", "dandere"): dandere_responses["relationship_status"],
        ("favorite_food", "dandere"): dandere_responses["favorite_food"],
        ("personality_quirks", "dandere"): dandere_responses["personality_quirks"],
        ("feeling", "himedere"): himedere_responses["feeling"],
        ("family", "himedere"): himedere_responses["family"],
        ("childhood", "himedere"): himedere_responses["childhood"],
        ("insult", "himedere"): himedere_responses["insult"],
        ("compliment", "himedere"): himedere_responses["compliment"],
        ("interest_manga", "himedere"): himedere_responses["interest_manga"],
        ("interest_anime", "himedere"): himedere_responses["interest_anime"],
        ("interest_games", "himedere"): himedere_responses["interest_games"],
        ("interest_cooking", "himedere"): himedere_responses["interest_cooking"],
        ("relationship_status", "himedere"): himedere_responses["relationship_status"],
        ("favorite_food", "himedere"): himedere_responses["favorite_food"],
        ("personality_quirks", "himedere"): himedere_responses["personality_quirks"],
        ("feeling", "deredere"): deredere_responses["feeling"],
        ("family", "deredere"): deredere_responses["family"],
        ("childhood", "deredere"): deredere_responses["childhood"],
        ("insult", "deredere"): deredere_responses["insult"],
        ("compliment", "deredere"): deredere_responses["compliment"],
        ("interest_manga", "deredere"): deredere_responses["interest_manga"],
        ("interest_anime", "deredere"): deredere_responses["interest_anime"],
        ("interest_games", "deredere"): deredere_responses["interest_games"],
        ("interest_cooking", "deredere"): deredere_responses["interest_cooking"],
        ("relationship_status", "deredere"): deredere_responses["relationship_status"],
        ("favorite_food", "deredere"): deredere_responses["favorite_food"],
        ("personality_quirks", "deredere"): deredere_responses["personality_quirks"],
    }