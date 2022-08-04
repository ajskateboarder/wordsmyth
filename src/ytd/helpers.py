import re
import time


def regex_search(text, pattern, group=1, default=None):
    match = re.search(pattern, text)
    return match.group(group) if match else default


def search_dict(partial, search_key):
    stack = [partial]
    while stack:
        current_item = stack.pop()
        if isinstance(current_item, dict):
            for key, value in current_item.items():
                if key == search_key:
                    yield value
                else:
                    stack.append(value)
        elif isinstance(current_item, list):
            for value in current_item:
                stack.append(value)


def ajax_request(session, endpoint, ytcfg, retries=5, sleep=20):
    url = (
        "https://www.youtube.com"
        + endpoint["commandMetadata"]["webCommandMetadata"]["apiUrl"]
    )

    data = {
        "context": ytcfg["INNERTUBE_CONTEXT"],
        "continuation": endpoint["continuationCommand"]["token"],
    }

    for _ in range(retries):
        response = session.post(
            url, params={"key": ytcfg["INNERTUBE_API_KEY"]}, json=data
        )
        if response.status_code == 200:
            return response.json()
        if response.status_code in [403, 413]:
            return {}
        else:
            time.sleep(sleep)
