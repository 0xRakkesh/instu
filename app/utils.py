import re 

def url_to_shortcode(url: str) -> str | None :

    pattern = r'/p/([A-Za-z0-9_-]+)'

    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None