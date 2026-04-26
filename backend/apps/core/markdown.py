import bleach
import markdown as md

ALLOWED_TAGS = ["p", "strong", "em", "br", "a", "ul", "ol", "li"]
ALLOWED_ATTRS = {"a": ["href", "title", "rel", "target"]}


def render_markdown(text: str) -> str:
    if not text:
        return ""
    html = md.markdown(text, extensions=["nl2br"])
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
