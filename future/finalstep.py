import json
import pandas as pd

df = pd.read_csv("./extracts.csv")

with open("./emojimap.json", "r", encoding="utf-8") as fh:
    em = json.load(fh)


def find_indices(content, classes):
    occurences = [e in content for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    return list(content.index(classes[i]) for i in indices)


# label emoji map with repr
em = {e["repr"]: e for e in em}

em[":cry:"]["sentiment"] = "neg"
em[":grimacing:"]["sentiment"] = "neu"

texts = df[["text", "emojis", "sentiment"]].to_dict("records")

incorrect = []
correct = []
fixed = []

# for every value in texts dict array:
for t in texts:
    emojis = t["emojis"].split(", ")

    # find positions where specific emojis show up
    maps = find_indices(emojis, [":confused:", ":thumbsup:", ":eyes:"])

    # if occurences show up once or twice
    if len(maps) == 2 or len(maps) == 1:
        reprr = emojis[min(maps)]
        match = em[reprr]

        obj = {
            "content": t["text"],
            "emoji": reprr,
            "position": min(maps),
            "sentiment": {"flair": t["sentiment"], "map": match["sentiment"]},
            "emojis": emojis,
            "matches": t["sentiment"] == match["sentiment"],
        }

        # check if flair sentiment doesn't equal emoji sentiment
        if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
            # find emojis that match flair sentiment
            sequence = list(
                obj["emojis"].index(em[e]["repr"])
                for e in emojis
                if em[e]["sentiment"] == t["sentiment"]
                and em[e]["repr"] in obj["emojis"]
            )

            newst = em.get(
                (obj["emojis"][min(sequence)] if len(sequence) > 0 else ""), {}
            )

            print([obj["emojis"][s] for s in sequence])
            if t["sentiment"] == newst.get("sentiment"):
                # print(obj["content"], t["sentiment"], newst.get("sentiment"), "\n")
                print(obj["content"], newst.get("emoji"), "\n")
                obj["fixed"] = newst.get("repr")
                fixed.append(obj)
            else:
                # print(obj["content"], newst.get("emoji"), "\n")
                # print(t["text"], t["sentiment"], newst.get("sentiment"))
                incorrect.append(obj)
        else:
            correct.append(obj)

with open("fixed.json", "w") as fh:
    json.dump(fixed, fh)
