--- a/src/tests/test_waifu_chatbot_class.py
+++ b/src/tests/test_waifu_chatbot_class.py
@@ -140,4 +140,14 @@
             self.chatbot.respond("how do you feel")
             if self.chatbot.current_dere != initial_dere:
                 self.assertNotEqual(self.chatbot.current_dere, initial_dere)
+
+    def test_integrated_conversation_topic_persistence(self):
+        # Start a conversation
+        with patch('random.random', return_value=0.1):
+            self.chatbot.respond("random input")
+            initial_topic = self.chatbot.current_topic
+            if initial_topic:
+                # Check that the topic persists to the next turn
+                response = self.chatbot.respond("something else")
+                self.assertIn(initial_topic, response)
+                self.assertIsNone(self.chatbot.current_topic)