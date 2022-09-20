from transformers import (
    RobertaTokenizerFast,
    TFRobertaForSequenceClassification,
    pipeline,
)
import pandas as pd

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline("sentiment-analysis", model="arpanghoshal/EmoRoBERTa")

df = pd.read_csv("final.csv")["content"]

print(df.apply(emotion))
