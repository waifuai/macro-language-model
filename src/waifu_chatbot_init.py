from core.registry import Registry
#from main_keywords import register_keywords
#from main_transforms import register_transforms
from dere_types import DereContext
from response_generator import ResponseGenerator

def initialize_personality(chatbot, personality: str):
    if personality == "deredere":
        from personalities.deredere.logic import DeredereLogic
        chatbot.personality = DeredereLogic(chatbot.debug)
    elif personality == "tsundere":
        from personalities.tsundere.logic import TsundereLogic
        chatbot.personality = TsundereLogic()
    elif personality == "yandere":
        from personalities.yandere.logic import YandereLogic
        chatbot.personality = YandereLogic()
    elif personality == "kuudere":
        from personalities.kuudere.logic import KuudereLogic
        chatbot.personality = KuudereLogic()
    elif personality == "dandere":
        from personalities.dandere.logic import DandereLogic
        chatbot.personality = DandereLogic()
    elif personality == "himedere":
        from personalities.himedere.logic import HimedereLogic
        chatbot.personality = HimedereLogic()
    else:
        raise ValueError(f"Invalid personality: {personality}")
    chatbot.current_dere = personality
    chatbot.dere_context = DereContext(chatbot.waifu_memory, chatbot.current_dere, set(), chatbot.debug)

def register_components(chatbot):
    chatbot.registry = Registry()
    #register_keywords(chatbot)
    #register_transforms(chatbot)
    chatbot.response_generator = ResponseGenerator(
        chatbot,
        chatbot.waifu_memory,
        {}, # Removed transformations
        chatbot.personality.talk_about_interest,  # Assuming personalities have this method
        chatbot.personality.introduce_topic,  # Assuming personalities have this method
        chatbot.personality.remember, # Assuming personalities have this method.
        chatbot.debug
    )
    #if chatbot.debug:
    #    print(f"WaifuChatbot.__init__: Keywords: {chatbot.registry.keywords}")
    #    print(f"WaifuChatbot.__init__: Transformations: {chatbot.registry.transformations}")