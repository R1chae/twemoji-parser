import emoji
from aiohttp import ClientSession

cdn_fmt = "https://twemoji.maxcdn.com/v/latest/72x72/{}.png"

async def valid_src(url, session):
    res = await session.head(url)
    return res.status == 200

def codepoint(codes):
    if "200d" not in codes:
        return "-".join([c for c in codes if c != "fe0f"])
    return "-".join(codes)

async def emoji_to_url(char, include_check=True, use_session=None, *args, **kwargs):
    src = cdn_fmt.format(codepoint(["{cp:x}".format(cp=ord(c)) for c in char]))
    if not include_check: return src
    session = ClientSession() if not use_session else use_session
    is_valid = await valid_src(src, session)

    if is_valid:
        return src
    return char