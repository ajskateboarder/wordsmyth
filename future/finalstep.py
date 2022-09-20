import json
import pandas as pd

df = pd.read_csv("./extracts.csv")

with open("./emojimap.json", "r", encoding="utf-8") as fh:
    em = json.load(fh)

em = {e["repr"]: e for e in em}
#em[":eyes:"]["sentiment"] = "neg"

texts = df[["text", "emojis", "sentiment"]]

vals = list(texts.to_dict().values())


objects = []
for t, e, s in zip(vals[0].values(), vals[1].values(), vals[2].values()):
    emojis = e.split(", ")

    classes = [":confused:", ":thumbsup:", ":eyes:"]
    occurences = [e in emojis for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    maps = list(emojis.index(classes[i]) for i in indices)

    if len(maps) == 2 or len(maps) == 1:
        reprr = emojis[min(maps)]
        match = em[reprr]

        if s != match["sentiment"]:
            obj = {
                "content": t,
                "emoji": reprr,
                "position": min(maps),
                "sentiment": {"flair": s, "map": match["sentiment"]},
                "emojis": emojis,
                "matches": s == match["sentiment"],
            }

            sequence = list(
                obj["emojis"].index(em[e]["repr"])
                for e in emojis
                if em[e]["sentiment"] == s and em[e]["repr"] in obj["emojis"]
            )
            print(
                f"{obj['content']}\n\n"
                f"TorchMoji gave {reprr}, and Flair gave {s}\n"
                f"{obj['emojis'][min(sequence)] if len(sequence) > 0 else ''} "
                "is a nicer option\n\n"
                f"{[obj['emojis'][s] for s in sequence]}\n\n"
                "********\n"
            )
            # print(
            #     obj["content"],
            #     "\n",
            #     reprr,
            #     s,
            #     "\n",
            #     obj["emojis"][min(sequence)] if len(sequence) > 0 else "",
            #     "\n",
            # )
            # pprint(obj)
            objects.append(obj)
