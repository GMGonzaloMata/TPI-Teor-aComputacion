import tkinter as tk
from tkinter import scrolledtext, messagebox
from lexer import lexer
from parser import Parser
from semantic import semantic_check
from pprint import pformat
from intermediate_code import generate_intermediate_code

class CompiladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Análisis Léxico, Sintáctico y Semántico")
        self.root.geometry("900x900")

        # Área de texto para el código fuente
        tk.Label(root, text="Código fuente:").pack(anchor="w", padx=10, pady=(10,0))
        self.text_area = scrolledtext.ScrolledText(root, height=12, width=110)
        self.text_area.pack(padx=10, pady=(0,10))

        # Botón para ejecutar el compilador
        self.run_button = tk.Button(root, text="Ejecutar compilador", command=self.ejecutar_compilador)
        self.run_button.pack(pady=5)

        # Definir las etapas
        self.etapas = [
            "Tokens (Léxico)",
            "AST (Sintáctico)",
            "Errores Semánticos",
            "Código Intermedio"
        ]
        self.resultados = {}
        self.frames = {}
        self.botones = {}

        # Crear acordeón
        for i, etapa in enumerate(self.etapas):
            btn = tk.Button(root, text=f"▶ {etapa}", anchor="w", width=120,
                            command=lambda e=etapa: self.toggle_etapa(e))
            btn.pack(fill="x", padx=10, pady=(5,0))
            self.botones[etapa] = btn

            frame = tk.Frame(root)
            salida = scrolledtext.ScrolledText(frame, height=8, width=110, state="disabled")
            salida.pack()
            self.resultados[etapa] = salida
            self.frames[etapa] = frame

        self.etapa_abierta = None
        self.toggle_etapa(self.etapas[0])  # Abrir la primera por defecto

    def toggle_etapa(self, etapa):
        # Minimizar todas
        for e in self.etapas:
            self.frames[e].pack_forget()
            self.botones[e].config(text=f"▶ {e}")
        # Desplegar la seleccionada
        self.frames[etapa].pack(fill="both", expand=True, padx=10, pady=(0,5))
        self.botones[etapa].config(text=f"▼ {etapa}")
        self.etapa_abierta = etapa

    def mostrar_resultado(self, etapa, texto):
        area = self.resultados[etapa]
        area.config(state="normal")
        area.delete(1.0, tk.END)
        area.insert(tk.END, texto)
        area.config(state="disabled")

    def ejecutar_compilador(self):
        codigo = self.text_area.get(1.0, tk.END)
        # Análisis léxico
        tokens = lexer(codigo)
        if isinstance(tokens, str):
            self.mostrar_resultado("Tokens (Léxico)", tokens)
            self.mostrar_resultado("AST (Sintáctico)", "No se pudo analizar sintácticamente por error léxico.")
            self.mostrar_resultado("Errores Semánticos", "No se pudo analizar semánticamente por error léxico.")
            self.mostrar_resultado("Código Intermedio", "No se pudo generar código intermedio por error léxico.")
            return
        self.mostrar_resultado("Tokens (Léxico)", pformat(tokens, width=100))
        # Análisis sintáctico
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            self.mostrar_resultado("AST (Sintáctico)", pformat(ast, width=100))
        except Exception as e:
            self.mostrar_resultado("AST (Sintáctico)", f"Error sintáctico: {str(e)}")
            self.mostrar_resultado("Errores Semánticos", "No se pudo analizar semánticamente por error sintáctico.")
            self.mostrar_resultado("Código Intermedio", "No se pudo generar código intermedio por error sintáctico.")
            return
        # Análisis semántico
        errores = semantic_check(ast)
        if errores:
            self.mostrar_resultado("Errores Semánticos", "\n".join(errores))
            self.mostrar_resultado("Código Intermedio", "No se pudo generar código intermedio por errores semánticos.")
        else:
            self.mostrar_resultado("Errores Semánticos", "Análisis semántico exitoso. Todo en orden.")
            # Generación de código intermedio
            codigo_intermedio = generate_intermediate_code(ast)
            self.mostrar_resultado("Código Intermedio", codigo_intermedio)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorGUI(root)
    root.mainloop() 