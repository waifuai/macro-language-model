import pytest
from memory import remember
from waifu_frame import WaifuFrame

@pytest.mark.parametrize("slot, value, affection_change, expected_affection", [
    ("name", "Alice", 0, 50),  # No affection change
    ("feeling", "love", 2, 55),  # 50 + 3 ("love") + 2
    ("feeling", "hate", -2, 46),  # 50 - 2 ("hate") - 2
    ("feeling", "love", 100, 100),  # Max 100
    ("feeling", "hate", -100, 0),  # Min 0
])
def test_remember(slot, value, affection_change, expected_affection):
    waifu_memory = WaifuFrame("Test")
    remember(waifu_memory, slot, value, affection_change)
    assert getattr(waifu_memory, slot) == value
    assert waifu_memory.affection == expected_affection