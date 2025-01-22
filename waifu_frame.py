class WaifuFrame:
    def __init__(self, name):
        self.name = name
        self.affection = 50
        self.interests = ["reading manga", "watching anime", "playing video games", "cooking"]
        self.hobbies = ["cosplay", "singing karaoke", "collecting anime figures"]
        self.memories = []
        self.relationship_status = "just friends"
        self.favorite_food = "pocky"
        self.personality_quirks = []  # Add a list for personality quirks

    def set_favorite_food(self, food):
        """Updates the waifu's favorite food."""
        self.favorite_food = food