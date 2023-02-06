# Abstract

A user review allows a consumer to publish their experience with a product or content. Reviews are usually accompanied by a star rating which summarize a user's comment into a simple value. The star ratings of each product review can then be averaged into a general star rating, which makes it even easier for potential consumers considering many different products. Star ratings also drive marketing and competing businesses on e-commerce websites. However, there are many occurences where star ratings are inconsistent with the text sentiment or just not applied to the platform, such as YouTube or SoundCloud. Natural language processing (NLP) is a subset of artificial intelligence which extracts data from unstructured text into a proper format. Wordsmyth, the tool presented here, fixes these issues by generating a rating based on the review content using NLP. Wordsmyth uses the Flair and TorchMoji NLP models that output sentiment information. It also uses the Emoji Sentiment Ranking that quantifies sentiment from most emojis. Wordsmyth can also be used as a framework which allows developers to write data collection logic for a platform and then process it with Flair and TorchMoji.

Wordsmyth answers these research questions:

- Can you apply NLP models to user reviews to generate accurate star ratings?
- Could this tool help automate marketing analytics?
- Is this tool easy to integrate with different platforms?

Wordsmyth's star rating accuracy is tested using Amazon review data (which have their own user ratings).
