from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax


class Roberta:
    def __init__(self):
        MODEL_SLUG = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_SLUG)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_SLUG)

    def predict(self, text):
        encoded_text = self.tokenizer(text, return_tensors="pt")
        output = self.model(**encoded_text)

        scores = softmax(output[0][0].detach().numpy())
        return {"neg": scores[0], "neu": scores[1], "pos": scores[2]}
