def generate_intermediate_code(ast):
    """
    Genera un código intermedio simple a partir del AST.
    Cada escena se convierte en una etiqueta y cada elección en una instrucción de salto.
    """
    if not ast:
        return "[Sin AST]"
    code = []
    for escena in ast:
        code.append(f"LABEL {escena['name']}")
        if escena['text']:
            code.append(f'  PRINT "{escena["text"]}"')
        for choice in escena['choices']:
            code.append(f'  CHOICE "{choice["text"]}"')
            code.append(f'  GOTO {choice["target"]}')
        code.append("")
    return "\n".join(code) 