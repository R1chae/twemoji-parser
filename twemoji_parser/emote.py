import unicodedata
import emoji
import requests

cdn_fmt = "https://twemoji.maxcdn.com/v/latest/72x72/{code}.png"

def valid_src(url):
    resp = requests.head(url)
    return resp.status_code == 200

def valid_category(char):
    try:
        return unicodedata.category(char) == "So"
    except:
        return False

def get_best_name(char):
    shortcode = emoji.demojize(char, use_aliases=True)
    return shortcode.replace(":", "").replace("_", " ").replace("selector", "").title()

def codepoint(codes):
    if "200d" not in codes:
        return "-".join([c for c in codes if c != "fe0f"])
    return "-".join(codes)

def emoji_to_url(char):
    if valid_category(char):
        name = unicodedata.name(char).title()
    else:
        if len(char) == 1:
            return None
        else:
            name = get_best_name(char)

    src = cdn_fmt.format(code=codepoint(["{cp:x}".format(cp=ord(c)) for c in char]))

    if valid_src(src):
        return src
    else:
        return None