class Gramatica:
    def __init__(self, terminales, no_terminales, producciones, simbolo_inicial):
        # Inicializa los simbolos terminales, no terminales, producciones y el simbolo inicial
        self.terminales = terminales
        self.no_terminales = no_terminales
        self.producciones = self.procesar_producciones(producciones)
        self.simbolo_inicial = simbolo_inicial
        self.derivacion_particular = []  # Almacena la derivación particular
        self.visitados = set()  # Para evitar ciclos en la derivación

    def procesar_producciones(self, producciones):
        # Procesa las producciones en un diccionario que agrupa alternativas
        prod_dict = {}
        for produccion in producciones:
            # Separa la parte izquierda y derecha de la producción
            izq, der = produccion.split("->")
            # cuadno existen diferentes producciones
            alternativas = der.split("|")
            if izq in prod_dict:
                prod_dict[izq].extend(alternativas)
            else:
                prod_dict[izq] = alternativas
        return prod_dict

    def pertenece_al_lenguaje(self, palabra):
        # Verifica si la palabra pertenece al lenguaje definido por la gramática
        self.derivacion_particular = []
        self.visitados = set()
        return self.derivar(self.simbolo_inicial, palabra)

    def derivar(self, actual, palabra, nivel=0):
        # Realiza la derivación de la cadena actual buscando la palabra que se necesita
        if (actual, palabra) in self.visitados:  # Si ya lo hemos visitado, evitar ciclos
            return False
        self.visitados.add((actual, palabra))
        self.derivacion_particular.append(actual)
        # Manejo de cadenas vacías
        if actual == '' and palabra == '':  # Si ambas cadenas están vacías, la derivación es válida
            return True

        if actual == palabra:
            return True

        if len(actual) > len(palabra):
            return False

        for i, simbolo in enumerate(actual):
            if simbolo in self.no_terminales:
                for produccion in self.producciones.get(simbolo, []):
                    nueva_palabra = actual[:i] + produccion + actual[i + 1:]
                    if self.derivar(nueva_palabra, palabra, nivel + 1):
                        return True

        # Probar la derivación con lambda o epsilon
        for simbolo in actual:
            if simbolo in self.no_terminales:
                for produccion in self.producciones.get(simbolo, []):
                    if produccion == '':  # Si hay una producción que genera epsilon
                        nueva_palabra = actual.replace(
                            simbolo, '', 1)  # Elimina el no terminal
                        if self.derivar(nueva_palabra, palabra, nivel + 1):
                            return True

        self.derivacion_particular.pop()
        return False

    def mostrar_arbol_derivacion(self):

        return ' -> '.join(self.derivacion_particular)

    def mostrar_arbol_sintesis(self, simbolo=None, nivel=0, max_nivel=4):
        # Muestra el árbol de derivación general
        if simbolo is None:
            simbolo = self.simbolo_inicial
        arbol = "    " * nivel + "|----" + simbolo + "\n"

        if nivel >= max_nivel:
            return arbol

        # Si el símbolo es un no terminal, se expande con todas las producciones
        for i, s in enumerate(simbolo):
            if s in self.no_terminales:
                for produccion in self.producciones.get(s, []):
                    nueva_palabra = simbolo[:i] + produccion + simbolo[i + 1:]
                    arbol += self.mostrar_arbol_sintesis(
                        nueva_palabra, nivel + 1, max_nivel)

        return arbol
