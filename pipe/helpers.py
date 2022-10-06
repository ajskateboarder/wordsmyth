from ast import literal_eval

def check_stdin(obj):
    obj = literal_eval(obj)
    if isinstance(obj[0][0], str):
        return "comments"
    if obj[0].get("sentiment"):
        return "flair"
    if obj[0].get("emojis"):
        return "torchmoji"
