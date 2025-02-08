import pytest
from dere_types import get_current_dere, maybe_change_dere, dere_response, DereContext
from waifu_frame import WaifuFrame
import random
from unittest.mock import patch

@pytest.mark.parametrize("affection, expected_dere", [
    (-10, "tsundere"),
    (-5, "yandere"),
    (0, "yandere"),
    (1, "kuudere"),
    (40, "kuudere"),
    (41, "dandere"),
    (75, "dandere"),
    (76, "deredere"),
    (100, "deredere"),
])
def test_get_current_dere(affection, expected_dere):
    assert get_current_dere(affection) == expected_dere

def test_maybe_change_dere_probability():
    waifu_memory = WaifuFrame("Test")
    current_dere = "yandere"
    dere_types = ["tsundere", "yandere"]
    used_responses = set()
    context = DereContext(waifu_memory, current_dere, used_responses, False)
    
    num_trials = 100
    change_count = 0
    for _ in range(num_trials):
        with patch('random.randint', return_value=0 if random.random() < 0.1 else 1):
            response = maybe_change_dere(context, dere_types)
            if context.current_dere != current_dere:
                change_count += 1
    # Probability of change should be around 10%
    assert 7 <= change_count <= 13

@pytest.mark.parametrize("current_dere, provided_responses, used_responses, expected_responses", [
    ("tsundere", ["B-baka!", "Hmph!"], set(), ["B-baka!", "Hmph!"]),
    ("yandere", [], set(), ["You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone."]),
    ("kuudere", [], {"Hmph."}, ["Hmph.", "...", "Is that so.", "I see.", "Understood."]),
    ("dandere", ["U-um..."], set(), ["U-um..."]),
    ("himedere", [], set(), ["Bow down to me, you peasant!", "You are lucky to be in my presence.", "Hmph, how amusing.", "Do as I command!", "You should be honored."]),
])
def test_dere_response(current_dere, provided_responses, used_responses, expected_responses):
    waifu_memory = WaifuFrame("Test")
    context = DereContext(waifu_memory, current_dere, used_responses, False)
    if provided_responses:
        response = dere_response(context, *provided_responses)
        assert response in provided_responses
    else:
        response = dere_response(context)
        assert response in expected_responses
    assert response in context.used_responses
    if len(used_responses) == 0:
        assert len(context.used_responses) == 1