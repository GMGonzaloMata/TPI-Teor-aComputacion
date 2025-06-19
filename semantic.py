def semantic_check(ast):
    errores = []

    nombres_de_escenas = set()
    referencias = []

    # Recolectar nombres y referencias
    for escena in ast:
        nombre = escena["name"]
        if nombre in nombres_de_escenas:
            errores.append(f"Nombre de escena duplicado: {nombre}")
        else:
            nombres_de_escenas.add(nombre)

        for choice in escena["choices"]:
            referencias.append((choice["target"], escena["name"]))

    # Verificar que todas las referencias existan
    for destino, origen in referencias:
        if destino not in nombres_de_escenas:
            errores.append(f"La escena '{origen}' hace referencia a una escena inexistente: '{destino}'")

    return errores
