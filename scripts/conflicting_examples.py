from src.wordsmyth import Pipeline

text = """I love my Brita filtration system. Bought it in Nov 2023 with a pack of replacement filters. I diligently follow the instructions by changing every 2 months and the correct filter placement. First two replacements were fine. The 3rd one filtered very fast (less than 30 seconds) and bubbles in the tank. I researched and found out the filter wasn't working properly. So, I put another new replacement filter in and it's doing the same thing. I've contacted Brita and they're sympathetic and sending me a new pack of filters. Just leery of buying more filters in case there's just a "bad batch" still out there. I will try one reviewer's suggestion about tilting the dispenser backwards."""
text2 = """Received this item quickly and exactly what we are looking for and needed.  Price is wonderful. My only drawback is it came packaged in an envelope style package.  The package was crushed during delivery process.  Please send in appropriate style packaging so the products don't get damaged."""

pipe = Pipeline()

item = pipe.predict(text2, as_object=True)
print(item._fix_content())
print(item.rating(exact=False))
