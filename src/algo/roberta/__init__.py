from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax


class Roberta:
    def __init__(self):
        MODEL_SLUG = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_SLUG)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_SLUG)

    def predict(self, text):
        if not isinstance(text, list):
            text = [text]

        encoded_text = self.tokenizer(text, return_tensors="pt")
        output = self.model(**encoded_text)

        scores = softmax(output[0][0].detach().numpy())
        return [scores[0], scores[1], scores[2]]
