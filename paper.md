# Wordsmyth - Applying NLP to user reviews to generate star ratings

## Rationale

A user review allows a consumer to publish their experience with a product or content. Reviews are usually accompanied by a star rating. These exist to summarize a user's writing into a simple star rating. The star ratings of each review of a product can then be averaged into a general star rating, which makes it even easier for potential consumers looking at many different products.

However, there are many occurences where star ratings are:

- inconsistent with the sentiment of the text, like [Amazon](https://amazon.com).
- not applied, such as [YouTube](https://youtube.com) or [SoundCloud](https://soundcloud.com).

Enter [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing), or NLP, a subset of artificial intelligence concerned with extracting data from unstructured text into a proper format.

Wordsmyth fixes the issues by generating a rating based on the **text content** itself. This is done using [Flair](https://github.com/flairNLP/flair) and [TorchMoji](https://github.com/huggingface/torchMoji) (PyTorch variant of [DeepMoji](https://github.com/bfelbo/DeepMoji)).

## Goals

Bruh

## Citations

```bibtex
@inproceedings{felbo2017,
  title={Using millions of emoji occurrences to learn any-domain representations for detecting sentiment, emotion and sarcasm},
  author={Felbo, Bjarke and Mislove, Alan and S{\o}gaard, Anders and Rahwan, Iyad and Lehmann, Sune},
  booktitle={Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year={2017}
}
```

```bibtex
@inproceedings{akbik2019flair,
  title={{FLAIR}: An easy-to-use framework for state-of-the-art {NLP}},
  author={Akbik, Alan and Bergmann, Tanja and Blythe, Duncan and Rasul, Kashif and Schweter, Stefan and Vollgraf, Roland},
  booktitle={{NAACL} 2019, 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations)},
  pages={54--59},
  year={2019}
}
```

```bibtex
@article{Kralj2015emojis,
  author={{Kralj Novak}, Petra and Smailovi{\'c}, Jasmina and Sluban, Borut and Mozeti\v{c}, Igor},
  title={Sentiment of emojis},
  journal={PLoS ONE},
  volume={10},
  number={12},
  pages={e0144296},
  url={http://dx.doi.org/10.1371/journal.pone.0144296},
  year={2015}
}
```
