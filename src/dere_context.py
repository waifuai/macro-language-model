from typing import NamedTuple, Set, Any

class DereContext(NamedTuple):
    waifu_memory: Any
    current_dere: str
    used_responses: Set[str]
    debug: bool