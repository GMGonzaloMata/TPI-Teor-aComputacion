class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def eat(self, expected_type):
        token = self.current_token()
        if token and token["type"] == expected_type:
            self.position += 1
            return token
        raise SyntaxError(f"Esperado {expected_type}, encontrado {token}")

    def parse(self):
        scenes = []
        while self.current_token():
            if self.current_token()["type"] == "NEWLINE":
                self.eat("NEWLINE")  # Ignora líneas vacías
                continue
            elif self.current_token()["type"] == "SCENE":
                scenes.append(self.parse_scene())
            else:
                raise SyntaxError(f"Esperado inicio de escena, encontrado {self.current_token()}")
        return scenes

    def parse_scene(self):
        # Ignorar líneas vacías al inicio
        while self.current_token() and self.current_token()["type"] == "NEWLINE":
            self.eat("NEWLINE")

        self.eat("SCENE")
        name_token = self.eat("IDENTIFIER")
        self.eat("COLON")

        text = None
        choices = []

     # Consumir líneas dentro de la escena
        while self.current_token():
            token_type = self.current_token()["type"]

            if token_type == "NEWLINE":
                self.eat("NEWLINE")
            elif token_type == "TEXT":
                self.eat("TEXT")
                string_token = self.eat("STRING")
                text = string_token["value"].strip('"')
            elif token_type == "CHOICE":
                choices.append(self.parse_choice())
            elif token_type == "SCENE":
                break  # Se terminó esta escena, comienza otra
            else:
                raise SyntaxError(f"Token inesperado dentro de escena: {self.current_token()}")

        return {
            "name": name_token["value"],
            "text": text,
            "choices": choices
     }


    def parse_choice(self):
        self.eat("CHOICE")
        string_token = self.eat("STRING")
        self.eat("ARROW")
        target_token = self.eat("IDENTIFIER")
        if self.current_token() and self.current_token()["type"] == "NEWLINE":
            self.eat("NEWLINE")

        return {
            "text": string_token["value"].strip('"'),
            "target": target_token["value"]
        }
