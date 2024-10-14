import tkinter as tk
from tkinter import messagebox, scrolledtext, font

from gramatica import Gramatica

class Interfaz:
    def __init__(self, master):
        self.master = master
        master.title("Verificador de Palabras")
        master.geometry("800x700")
        master.configure(bg="#ebeced")

        self.title_font = font.Font(family="Arial", size=18, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.entry_font = font.Font(family="Arial", size=10)

        outer_frame = tk.Frame(master, bg="blue")
        outer_frame.pack(expand=True) 

        contenedor = tk.Frame(outer_frame, bg="#fafafa", bd=2, relief="flat", padx=20, pady=10)
        contenedor.pack(pady=0)

        tk.Label(contenedor, text="Generador de Árboles y Verificador de Palabras", font=self.title_font, bg="#fafafa", fg="#333", pady=20).pack()

        container = tk.Frame(contenedor, bg="#fafafa")
        container.pack(pady=20)

        self.add_input("Símbolos Terminales (separados por comas):", container)
        self.entry_terminales = self.create_entry(container)

        self.add_input("Símbolos No Terminales (separados por comas):", container)
        self.entry_no_terminales = self.create_entry(container)

        self.add_input("Producciones (A->B, separadas por comas):", container)
        self.entry_producciones = self.create_entry(container)

        self.add_input("Símbolo Inicial:", container)
        self.entry_simbolo_inicial = self.create_entry(container)

        self.add_input("Palabra a Verificar (w):", container)
        self.entry_palabra = self.create_entry(container)

        self.add_input("Nivel Máximo del Árbol de sintesis:", container)
        self.entry_nivel_maximo = self.create_entry(container)

        btn_verificar = tk.Button(contenedor, text="Verificar Palabra", command=self.verificar_palabra, bg="#4CAF50", fg="#fafafa", font = font.Font(family="Arial", size=12, weight="bold") , padx=10, pady=10, relief="flat")
        btn_verificar.pack(pady=15)

        self.text_area = scrolledtext.ScrolledText(contenedor, width=65, height=15, font=self.entry_font, relief="flat", borderwidth=1, wrap=tk.WORD)
        self.text_area.pack(pady=20)

    def add_input(self, text, container):
        """Helper function to add a label and an entry field."""
        tk.Label(container, text=text, font=self.label_font, bg="#fafafa", fg="#333").pack(anchor='w', pady=5)

    def create_entry(self, container):
        """Helper function to create a modern-looking entry field.""" 
        entry = tk.Entry(container, font=self.entry_font)
        entry.pack(fill=tk.X, pady=5, ipady=5)
        return entry

    def verificar_palabra(self):
        terminales = self.entry_terminales.get().split(',')
        no_terminales = self.entry_no_terminales.get().split(',')
        producciones = self.entry_producciones.get().split(',')
        simbolo_inicial = self.entry_simbolo_inicial.get()
        palabra = self.entry_palabra.get()
        max_nivel = int(self.entry_nivel_maximo.get())

        if len(terminales) < 1:
            messagebox.showerror("Error", "Se deben ingresar al menos 1 símbolo terminal.")
            return
        if len(no_terminales) < 1:
            messagebox.showerror("Error", "Se deben ingresar al menos 1 símbolo no terminal.")
            return
        if len(producciones) < 1:
            messagebox.showerror("Error", "Se deben ingresar al menos 1 producción.")
            return

        gramatica = Gramatica(terminales, no_terminales, producciones, simbolo_inicial)

        pertenece = gramatica.pertenece_al_lenguaje(palabra)
        resultado_text = f"w='{palabra}' {': W ∈ L -> Pertenece' if pertenece else ': NO pertenece'} al lenguaje.\n"
        resultado_text += "Árbol de derivación:\n"
        resultado_text += gramatica.mostrar_arbol_derivacion()
        resultado_text += "\nÁrbol de sintesis:\n" + gramatica.mostrar_arbol_sintesis(max_nivel=max_nivel)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, resultado_text)

ventana = tk.Tk()
interfaz = Interfaz(ventana)

ventana.mainloop()
