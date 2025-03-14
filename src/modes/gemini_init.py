from waifu_chatbot import WaifuChatbot

def initialize_chatbot(waifu_name: str, debug: bool):
    waifu = WaifuChatbot(waifu_name, debug=debug)
    return waifu