import unittest
from waifu_chatbot import WaifuChatbot

class TestWaifuChatbotMinimal(unittest.TestCase):
    def test_basic_import(self):
        chatbot = WaifuChatbot("TestWaifu", debug=True)
        self.assertIsNotNone(chatbot)

if __name__ == '__main__':
    unittest.main()