import re

TOKEN_REGEX = [
    ("SCENE", r"\bscene\b"),
    ("TEXT", r"\btext\b"),
    ("CHOICE", r"\bchoice\b"),
    ("END", r"\bend\b"),
    ("ARROW", r"->"),
    ("COLON", r":"),
    ("STRING", r'"[^"\n]*"'),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
]

def lexer(code):
    tokens = []
    index = 0
    while index < len(code):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(code, index)
            if match:
                if token_type != "WHITESPACE":
                    tokens.append({
                        "type": token_type,
                        "value": match.group(0),
                        "position": index
                    })
                index = match.end()
                break
        if not match:
            return (f"Carácter inesperado: '{code[index]}' en posición {index}")
    return tokens
