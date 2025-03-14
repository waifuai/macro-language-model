def register_interests_keywords(waifu):
    waifu.registry.defkeyword("interest_manga", ["interest_manga"])
    waifu.registry.defkeyword("interest_anime", ["interest_anime"])
    waifu.registry.defkeyword("interest_games", ["interest_games"])
    waifu.registry.defkeyword("interest_cooking", ["interest_cooking"])
    waifu.registry.defsynonym("like", "enjoy", "love", "adore", "appreciate")
    waifu.registry.defsynonym("hate", "dislike", "despise", "loathe", "abhor")