import sqlite3
import json

db = sqlite3.connect("dumped.db")
query = db.cursor()

def extract():
    with open("data.json", encoding="utf-8") as fh:
        data = json.load(fh)
    return [(comment["content"], comment["emoji"],
              comment["sentiment"]["flair"], comment["sentiment"]["map"], ",".join(
                  comment["emojis"]),
              comment["matches"], comment["status"], comment["score"], comment["rating"]) for comment in data]


def load(data):
    query.executemany("INSERT INTO comments VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
    db.commit()
        

if __name__ == "__main__":
    comments = extract()
    load(comments)
