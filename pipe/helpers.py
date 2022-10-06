from ast import literal_eval

def convert_stdin(obj):
    obj = literal_eval(obj)
    return obj
