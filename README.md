<picture>
<source media="(prefers-color-scheme: dark)" srcset="./media/logo_dark.svg" width=130 align=right />
<img alt="The Wordsmyth logo" src="./media/logo.svg" align="right" width=130>
</picture>

# Wordsmyth

Wordsmyth eases the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, Wordsmyth *generates them* based on the text sentiment by applying pre-trained neural network results to hardcoded rule-based analysis, a process known as transfer learning. This combination of data analysis results in high-accuracy rating prediction that handles sarcasm. (for the most part)

Wordsmyth functions as a modular pipeline with a focus on being easy to maintain and extend.

## Usage with Python

Install the pre-requisites:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./helper model # downloads the TorchMoji model locally
```

and use the module like so:

```py
import wordsmyth

pipe = wordsmyth.Pipeline()
content = pipe.eval("LOL")
print(content.rating()) # 0.5
```

## Caveats

Slight issues with the algorithm which can possibly be fixed in the future.

### Vague comments

Comments like `ok` and `cheap` are impossible to infer without a user's star rating. The context of these reviews can't be discerned.

Examples:

| content       | predicted     | actual |
| ------------- | ------------- | ------ |
| ok part       | 4.0070        | 2      |
| cheap         | 4.5680        | 3      |
| ok            | 5.3333        | 3      |

The definition of an okay or cheap product is subjective, and Flair mostly leans toward the positive definition of these words.

**Possible fix:** Exclude the content from analysis in e-commerce context based on a word limit.

### Irregular tone shifts in sentiment

Text that quickly changes in tone can sometimes be incorrectly predicted by the algorithm stack, especially in the case of Flair.

An example of this type of text would include:

| content       | predicted     | actual |
| ------------- | ------------- | ------ |
| works great. we loved ours! till we didn't. these do not last so buy the warranty as you WILL NEED IT. | 4.3935 | 2
| Luved it for the few months it worked! great little bullet shaped ice cubes. It was a gift for my sister who never opened the box. The next summer during a heat wave I asked for my unused gift back, ha!, and was in heaven for a few months. the next summer after a few weeks the unit gave out... | 4.7115 | 2 |

**Possible fix:** Tokenize the content into sentences instead of predicting the content as a whole. This should only be applied in particular cases since it would be more computationally expensive.
