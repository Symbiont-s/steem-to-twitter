REPLACE = {
   "['": "#",
   ", '":"#",
   "']":"",
   "'":" ",
   "[]":"",
}

def from_list_to_str(lista: list, replace: dict = REPLACE):
    string = str(lista)
    for key in replace:
        string = string.replace(key, replace[key])
    return string

def category_is_empty(category, tags):
    if not category:
        if len(tags) > 0:
            category = tags[0]
    return category

def build_url(base_url: str, author: str, permlink: str, category: str):
    prefix = "" if base_url.endswith("/") else "/"
    url = f'{base_url}{prefix}{category + "/" if category else ""}@{author}/{permlink}'
    return url

def required_tags(post_tags, list_tags):
    """
    Check that at least one of the tags of a post is in the list of required tags
 
        :param list post_tags: post tags
        :param list list_tags: Required tags
    """
    if list_tags:
        for tag in post_tags:
            if tag in list_tags:
                return True
        return False
    return True

def empty_json(path):
    try:
        with open(path, 'w') as file: 
            pass
    except Exception:
        pass