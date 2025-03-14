from .general import register_general_transforms
from .family import register_family_transforms
from .childhood import register_childhood_transforms
from .feelings import register_feelings_transforms
from .interests import register_interests_transforms
from .relationship import register_relationship_transforms
from .food import register_food_transforms
from .quirks import register_quirks_transforms

__all__ = [
    "register_general_transforms",
    "register_family_transforms",
    "register_childhood_transforms",
    "register_feelings_transforms",
    "register_interests_transforms",
    "register_relationship_transforms",
    "register_food_transforms",
    "register_quirks_transforms"
]