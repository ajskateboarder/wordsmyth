import json
import pandas as pd

df = pd.read_csv("./poop.csv")

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
print(df.keys())

texts = df[["text", "emojis", "sentiment", "score"]].to_dict("records")
print(texts)

incorrect = []
correct = []
fixed = []

# for every value in texts dict array:
for t in texts:
    emojis = t["emojis"].split(",")

    # find positions where specific emojis show up
    maps = find_indices(emojis, [":confused:", ":thumbsup:", ":eyes:"])
    print(maps)

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
            "score": t["score"],
        }
        print(obj)

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
                obj["status"] = "fixed"
                fixed.append(obj)
            else:
                # print(obj["content"], newst.get("emoji"), "\n")
                # print(t["text"], t["sentiment"], newst.get("sentiment"))
                obj["status"] = "incorrect"
                incorrect.append(obj)
        else:
            obj["status"] = "correct"
            correct.append(obj)

with open("data.json", "w") as fh:
    json.dump([*incorrect, *correct, *fixed], fh)