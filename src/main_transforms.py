from typing import Any, List

from transformations import deftransform

def register_transforms(waifu: Any) -> None:
    """Registers transformations for the waifu chatbot.

    Args:
        waifu: The waifu chatbot object.
    """
    deftransform(waifu.registry.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name")
    deftransform(waifu.registry.transformations, "i am feeling *", ["Oh, you're feeling *."], memory_slot="feeling")
    deftransform(waifu.registry.transformations, "i like *", ["Oh, you like *? Tell me more!"], memory_slot="likes", affection_change=2)
    deftransform(waifu.registry.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.registry.transformations, "what is my name", ["waifu-memory", "name"])
    deftransform(waifu.registry.transformations, "what is my feeling", ["waifu-memory", "feeling"])
    deftransform(waifu.registry.transformations, "tell me about my likes", ["waifu-memory", "likes"])
    deftransform(waifu.registry.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"])
    deftransform(waifu.registry.transformations, "talk about family", ["introduce-topic", "family"])
    deftransform(waifu.registry.transformations, "talk about childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.registry.transformations, "how do you feel", ["maybe-change-dere", "I'm doing great, thanks for asking!", "I'm feeling alright.", "Not too bad."])
    deftransform(waifu.registry.transformations, "tell me about your interests", ["talk-about"])
    deftransform(waifu.registry.transformations, "what is your relationship status", ["introduce-topic", "relationship_status"])
    deftransform(waifu.registry.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.registry.transformations, "tell me about your personality", ["waifu-memory", "personality_quirks"])
    deftransform(waifu.registry.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    # Add more general transformations
    deftransform(waifu.registry.transformations, "i am *", ["Why are you *?", "How long have you been *?"], affection_change=1)
    deftransform(waifu.registry.transformations, "i feel *", ["Why do you feel *?", "I'm here for you."], affection_change=1)
    # Add affection changes to existing transformations
    deftransform(waifu.registry.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"], affection_change=1)
    deftransform(waifu.registry.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name", affection_change=1)

    # Transformations for agreement/disagreement
    deftransform(waifu.registry.transformations, "yes", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.registry.transformations, "yeah", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.registry.transformations, "yep", ["I agree!", "Yeah!", "Sounds good!"], affection_change=1)
    deftransform(waifu.registry.transformations, "no", ["Oh, really?", "I see...", "Hmm."], affection_change=-1)
    deftransform(waifu.registry.transformations, "nope", ["Oh, really?", "I see...", "Hmm."], affection_change=-1)
    deftransform(waifu.registry.transformations, "i agree", ["That's great!", "I'm glad we agree."])
    deftransform(waifu.registry.transformations, "i disagree", ["Oh, that's interesting.", "Why do you think that?"])
    deftransform(waifu.registry.transformations, "you are right", ["Of course I am!", "I know, right?"])
    deftransform(waifu.registry.transformations, "you are wrong", ["Am not!", "I disagree."])

    # Transformations for handling questions
    deftransform(waifu.registry.transformations, "who is *", ["I don't know who * is.", "Who are you talking about?"])
    deftransform(waifu.registry.transformations, "what is *", ["I'm not sure what * is.", "What are you referring to?"])
    deftransform(waifu.registry.transformations, "where is *", ["I don't know where * is.", "Where is that?"])
    deftransform(waifu.registry.transformations, "when is *", ["I don't remember when * is.", "When was that?"])
    deftransform(waifu.registry.transformations, "why is *", ["I don't know why * is.", "Why do you ask?"])
    deftransform(waifu.registry.transformations, "how is *", ["I don't know how * is.", "How is that possible?"])

    # Transformations for family topic
    deftransform(waifu.registry.transformations, "tell me about your family", ["introduce-topic", "family"])
    deftransform(waifu.registry.transformations, "do you have siblings", ["Do *you* have siblings?", "I'm not sure, do you?"])
    deftransform(waifu.registry.transformations, "what are your parents like", ["They're... parents. What are *your* parents like?"])
    deftransform(waifu.registry.transformations, "my family is *", ["Oh, your family is *? Mine is complicated."])

    # Transformations for childhood topic
    deftransform(waifu.registry.transformations, "tell me about your childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.registry.transformations, "what was your childhood like", ["It was a childhood. What was *yours* like?"])
    deftransform(waifu.registry.transformations, "i had a * childhood", ["Oh, you had a * childhood? Mine was pretty normal."])
    deftransform(waifu.registry.transformations, "did you have a good childhood", ["Did *you* have a good childhood?", "It was alright, I guess."])

    # Transformations for feelings topic
    deftransform(waifu.registry.transformations, "i am feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])
    deftransform(waifu.registry.transformations, "are you feeling *", ["maybe-change-dere", "Why do you ask?", "I'm feeling... complicated."])
    deftransform(waifu.registry.transformations, "i'm feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])

    # Transformations for interests topic
    deftransform(waifu.registry.transformations, "what are your interests", ["talk-about"])
    deftransform(waifu.registry.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.registry.transformations, "i like to *", ["Oh, you like to *? That's interesting."])
    deftransform(waifu.registry.transformations, "i enjoy *", ["Oh, you enjoy *? Tell me more."])

    # Transformations for relationship topic
    deftransform(waifu.registry.transformations, "are you in a relationship", ["maybe-change-dere", "Why do you ask? Are *you* in a relationship?", "That's a personal question!"])
    deftransform(waifu.registry.transformations, "do you have a boyfriend", ["maybe-change-dere", "Do *you* have a boyfriend?", "That's none of your business!"])
    deftransform(waifu.registry.transformations, "do you have a girlfriend", ["maybe-change-dere", "Do *you* have a girlfriend?", "That's none of your business!"])
    deftransform(waifu.registry.transformations, "i have a *", ["Oh, you have a *? That's nice."])

    # Transformations for food topic
    deftransform(waifu.registry.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.registry.transformations, "do you like *", [("generate", "food")], [("food", "*")]) # Use "generate"
    deftransform(waifu.registry.transformations, "i like to eat *", ["Oh, you like to eat *? I've never tried that."])
    deftransform(waifu.registry.transformations, "i'm hungry", ["Maybe you should eat something.", "What are you hungry for?"])

    # Transformations for quirks topic
    deftransform(waifu.registry.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    deftransform(waifu.registry.transformations, "you are *", ["Am I? And how does that make you feel?"]) # More open-ended

    # Transformations to encourage questions and direct responses
    deftransform(waifu.registry.transformations, "what do you mean", ["maybe-change-dere", "What do *you* think I mean?", "I'm not sure what you're asking."])
    deftransform(waifu.registry.transformations, "what do you think", ["maybe-change-dere", "I'm not sure yet. What are your thoughts?", "I haven't made up my mind. What do you think?"])
    deftransform(waifu.registry.transformations, "are you sure", ["maybe-change-dere", "Are *you* sure?", "I'm as sure as I can be."])
    deftransform(waifu.registry.transformations, "is that so", ["maybe-change-dere", "Is it?", "That's what I heard."])
    deftransform(waifu.registry.transformations, "really", ["maybe-change-dere", "Really!", "Is that surprising?"])
    deftransform(waifu.registry.transformations, "tell me more", ["Tell you more about what, specifically?", "What are you curious about?"])
    deftransform(waifu.registry.transformations, "i don't know", ["You don't know? Maybe we can figure it out together.", "It's okay not to know everything."])
    deftransform(waifu.registry.transformations, "i'm not sure", ["What are you unsure about?", "Maybe I can help you figure it out."])
    deftransform(waifu.registry.transformations, "can you help me", ["maybe-change-dere", "I can try. What do you need help with?", "What kind of help are you looking for?"])
    deftransform(waifu.registry.transformations, "can you tell me", ["maybe-change-dere", "Tell you what?", "What do you want me to tell you?"])