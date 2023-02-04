# Wordsmyth - Applying NLP to user reviews to generate star ratings

## Rationale

A user review allows a consumer to publish their experience with a product or content. Reviews are usually accompanied by a star rating. These exist to summarize a user's writing into a simple star rating. The star ratings of each review of a product can then be averaged into a general star rating, which makes it even easier for potential consumers looking at many different products. Star ratings also drive marketing and competing businesses on e-commerce websites.

However, there are many occurences where star ratings are:

- inconsistent with the sentiment of the text, like [Amazon](https://amazon.com).
- not applied, such as [YouTube](https://youtube.com) or [SoundCloud](https://soundcloud.com).

Enter [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing), or NLP, a subset of artificial intelligence concerned with extracting data from unstructured text into a proper format.

WordSmyth uses [Flair](https://github.com/flairNLP/flair) and [TorchMoji](https://github.com/huggingface/torchMoji) (PyTorch variant of [DeepMoji](https://github.com/bfelbo/DeepMoji)), both of which are NLP models which output sentiment information. It also uses the [Emoji Sentiment Ranking](https://kt.ijs.si/data/Emoji_sentiment_ranking/) for translating TorchMoji emoji output into a decimal sentiment score.

Wordsmyth fixes the issues by generating a rating based on the **review content** using these models. This functions as a framework which allows developers to write data collection logic for their favorite platform and pipe it to the general algorithms.

This tool helps consumers discover quality content on platforms without pre-existing star ratings. For example, if a consumer is looking for a video tutorial on YouTube, the star rating can guide them to find the best one. This is especially useful in this case because of YouTube's [removal of the dislike button](https://www.youtube.com/watch?v=kxOuG8jMIgI).

It also helps businesses boost their marketing research since the value of some content is easily summarized. 

## Research Questions

- Can you apply NLP models to user reviews to create accurate star ratings?
- Could this tool remove the need for implementing a star rating system?
- Is this tool easy to integrate with different platforms?

This tool attempts to solve above mentioned issues with the traditional star rating system.

## Procedure

With a single comment:

1. Download comment/review data.
2. Pass comments through Flair and TorchMoji for processing.
3. Finetune the combined output of the algorithms.
4. Convert TorchMoji's emoji output into refinedsentiment data - positive, neutral, and negative percentages - using the Emoji Sentiment Ranking.
5. Analyze the combined data and generate a star rating from conditions found in the comment.

## Data

Wordsmyth uses:

- review data from online platforms, like YouTube comments
- the output from TorchMoji and Flair as well
- the Emoji Sentiment Ranking for converting TorchMoji data

## Citations

Felbo, B., Mislove, A., Søgaard, A., Rahwan, I., & Lehmann, S. (2017). Using millions of emoji occurrences to learn any-domain representations for detecting sentiment, emotion and sarcasm. In Conference on Empirical Methods in Natural Language Processing (EMNLP). ([paper](http://dx.doi.org/10.1371/journal.pone.0144296))

Akbik, A., Bergmann, T., Blythe, D., Rasul, K., Schweter, S., & Vollgraf, R. (2019). FLAIR: An easy-to-use framework for state-of-the-art NLP. In NAACL 2019, 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations) (pp. 54–59). ([paper](https://www.aclweb.org/anthology/papers/N/N19/N19-4010/))

Kralj Novak, P., Smailovic, J., Sluban, B., & Mozetič, I. (2015). Sentiment of emojis. PLoS ONE, 10(12), e0144296.
