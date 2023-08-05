from textblob import TextBlob
from statistics import mean

b = TextBlob("It works great for picking up any and all crumbs")
p = TextBlob("but it gets disgusting after 2 uses.")
print(mean([b.sentiment.polarity, p.sentiment.polarity]))
