from algo.roberta import Roberta

r = Roberta()


def roberta(texts):
    response = [
        str(r.predict(text)).replace("[", "").replace("]", "") for text in texts
    ]
    print(response)


roberta([["pooop"], ["pooop"]])
