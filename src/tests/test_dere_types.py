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

    # Use side_effect to simulate 10% chance.  Define OUTSIDE the loop.
    def mock_randint(a, b):
        return 0 if random.random() < 0.1 else 1

    with patch('dere_types.random.randint', side_effect=mock_randint):
        for _ in range(num_trials):
            response = maybe_change_dere(context, dere_types)
            new_dere = context.current_dere
            if new_dere != current_dere:
                change_count += 1
                context = context._replace(current_dere=new_dere)

    # Probability of change should be around 10%
    assert 5 <= change_count <= 15