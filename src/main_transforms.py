from typing import Any, List

from transformations import deftransform

def register_transforms(waifu: Any) -> None:
    """Registers transformations for the waifu chatbot.

    Args:
        waifu: The waifu chatbot object.
    """
    deftransform(waifu.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name")
    deftransform(waifu.transformations, "i am feeling *", ["Oh, you're feeling *."], memory_slot="feeling")
    deftransform(waifu.transformations, "i like *", ["Oh, you like *."], memory_slot="likes", affection_change=2)
    deftransform(waifu.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.transformations, "what is my name", ["waifu-memory", "name"])
    deftransform(waifu.transformations, "what is my feeling", ["waifu-memory", "feeling"])
    deftransform(waifu.transformations, "tell me about my likes", ["waifu-memory", "likes"])
    deftransform(waifu.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"])
    deftransform(waifu.transformations, "talk about family", ["introduce-topic", "family"])
    deftransform(waifu.transformations, "talk about childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.transformations, "how do you feel", ["maybe-change-dere", "I'm doing great, thanks for asking!", "I'm feeling alright.", "Not too bad."])
    deftransform(waifu.transformations, "tell me about your interests", ["talk-about"])
    deftransform(waifu.transformations, "what is your relationship status", ["introduce-topic", "relationship_status"])
    deftransform(waifu.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.transformations, "tell me about your personality", ["waifu-memory", "personality_quirks"])
    deftransform(waifu.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    # Add more general transformations
    deftransform(waifu.transformations, "i am *", ["Why are you *?", "How long have you been *?"], affection_change=1)
    deftransform(waifu.transformations, "i feel *", ["Why do you feel *?", "I'm here for you."], affection_change=1)
    # Add affection changes to existing transformations
    deftransform(waifu.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"], affection_change=1)
    deftransform(waifu.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name", affection_change=1)

    # Transformations for agreement/disagreement
    deftransform(waifu.transformations, "yes", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.transformations, "yeah", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.transformations, "yep", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.transformations, "no", ["Oh, really?", "I see...", "Hmm."], affection_change=-1)
    deftransform(waifu.transformations, "nope", ["Oh, really?", "I see...", "Hmm."], affection_change=-1)
    deftransform(waifu.transformations, "i agree", ["That's great!", "I'm glad we agree."])
    deftransform(waifu.transformations, "i disagree", ["Oh, that's interesting.", "Why do you think that?"])
    deftransform(waifu.transformations, "you are right", ["Of course I am!", "I know, right?"])
    deftransform(waifu.transformations, "you are wrong", ["Am not!", "I disagree."])

    # Transformations for handling questions
    deftransform(waifu.transformations, "who is *", ["I don't know who * is.", "Who are you talking about?"])
    deftransform(waifu.transformations, "what is *", ["I'm not sure what * is.", "What are you referring to?"])
    deftransform(waifu.transformations, "where is *", ["I don't know where * is.", "Where is that?"])
    deftransform(waifu.transformations, "when is *", ["I don't remember when * is.", "When was that?"])
    deftransform(waifu.transformations, "why is *", ["I don't know why * is.", "Why do you ask?"])
    deftransform(waifu.transformations, "how is *", ["I don't know how * is.", "How is that possible?"])

    # Transformations for family topic
    deftransform(waifu.transformations, "tell me about your family", ["introduce-topic", "family"])
    deftransform(waifu.transformations, "do you have siblings", ["Do *you* have siblings?", "I'm not sure, do you?"])
    deftransform(waifu.transformations, "what are your parents like", ["They're... parents. What are *your* parents like?"])
    deftransform(waifu.transformations, "my family is *", ["Oh, your family is *? Mine is complicated."])

    # Transformations for childhood topic
    deftransform(waifu.transformations, "tell me about your childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.transformations, "what was your childhood like", ["It was a childhood. What was *yours* like?"])
    deftransform(waifu.transformations, "i had a * childhood", ["Oh, you had a * childhood? Mine was pretty normal."])
    deftransform(waifu.transformations, "did you have a good childhood", ["Did *you* have a good childhood?", "It was alright, I guess."])

    # Transformations for feelings topic
    deftransform(waifu.transformations, "i am feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])
    deftransform(waifu.transformations, "are you feeling *", ["maybe-change-dere", "Why do you ask?", "I'm feeling... complicated."])
    deftransform(waifu.transformations, "i'm feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])

    # Transformations for interests topic
    deftransform(waifu.transformations, "what are your interests", ["talk-about"])
    deftransform(waifu.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.transformations, "i like to *", ["Oh, you like to *? That's interesting."])
    deftransform(waifu.transformations, "i enjoy *", ["Oh, you enjoy *? Tell me more."])

    # Transformations for relationship topic
    deftransform(waifu.transformations, "are you in a relationship", ["maybe-change-dere", "Why do you ask? Are *you* in a relationship?", "That's a personal question!"])
    deftransform(waifu.transformations, "do you have a boyfriend", ["maybe-change-dere", "Do *you* have a boyfriend?", "That's none of your business!"])
    deftransform(waifu.transformations, "do you have a girlfriend", ["maybe-change-dere", "Do *you* have a girlfriend?", "That's none of your business!"])
    deftransform(waifu.transformations, "i have a *", ["Oh, you have a *? That's nice."])

    # Transformations for food topic
    deftransform(waifu.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.transformations, "do you like *", [("generate", "food")], [("food", "*")]) # Use "generate"
    deftransform(waifu.transformations, "i like to eat *", ["Oh, you like to eat *? I've never tried that."])
    deftransform(waifu.transformations, "i'm hungry", ["Maybe you should eat something.", "What are you hungry for?"])

    # Transformations for quirks topic
    deftransform(waifu.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    deftransform(waifu.transformations, "you are *", ["Am I? And how does that make you feel?"]) # More open-ended

    # Transformations to encourage questions and direct responses
    deftransform(waifu.transformations, "what do you mean", ["maybe-change-dere", "What do *you* think I mean?", "I'm not sure what you're asking."])
    deftransform(waifu.transformations, "what do you think", ["maybe-change-dere", "I'm not sure yet. What are your thoughts?", "I haven't made up my mind. What do you think?"])
    deftransform(waifu.transformations, "are you sure", ["maybe-change-dere", "Are *you* sure?", "I'm as sure as I can be."])
    deftransform(waifu.transformations, "is that so", ["maybe-change-dere", "Is it?", "That's what I heard."])
    deftransform(waifu.transformations, "really", ["maybe-change-dere", "Really!", "Is that surprising?"])
    deftransform(waifu.transformations, "tell me more", ["Tell you more about what, specifically?", "What are you curious about?"])
    deftransform(waifu.transformations, "i don't know", ["You don't know? Maybe we can figure it out together.", "It's okay not to know everything."])
    deftransform(waifu.transformations, "i'm not sure", ["What are you unsure about?", "Maybe I can help you figure it out."])
    deftransform(waifu.transformations, "can you help me", ["maybe-change-dere", "I can try. What do you need help with?", "What kind of help are you looking for?"])
    deftransform(waifu.transformations, "can you tell me", ["maybe-change-dere", "Tell you what?", "What do you want me to tell you?"])