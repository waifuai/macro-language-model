from typing import List, Set, Tuple, NamedTuple, Any

class DereContext(NamedTuple):
    waifu_memory: Any
    current_dere: str
    used_responses: Set[str]
    debug: bool

from dere_data import dere_types