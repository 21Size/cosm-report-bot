import re


def escape_markdown(text: str) -> str:
    return re.sub(r'([_*\[\]()~>#+\-=|{}.!])', r'\\\1', text)


is_all_numbers = lambda lst: all(s.isdigit() for s in lst)
