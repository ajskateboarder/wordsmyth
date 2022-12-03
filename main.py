from json_api_doc import serialize


def jsonapi():
    def inner(f):
        def decorator_f(*args, **kwargs):
            return serialize(f())

        return decorator_f

    return inner


@jsonapi()
def thing():
    return {"$type": "submission", "hello": "world"}


print(thing())
