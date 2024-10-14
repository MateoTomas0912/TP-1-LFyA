class Gramatica:
    #Incializamos variables necesarias para la gramatica.
    def __init__(self):
        self.producciones = {}
        self.first = {}
        self.follow = {}
        self.select = {}
        self.EsLL1 = True #Nos dira si la gramatica es LL(1).

    #Se carga la gramatica y se calculan sus FIRST, FOLLOW y SELECT.
    def setear(self, string):
        reglas = string.strip().split("\n") #Divide las reglas por lineas.
        for regla in reglas:
            nt, derivacion = regla.split(":") # No terminal : derivacion
            nt = nt.strip()
            derivacion = derivacion.strip().split() #La derivacion en una lista de simbolos.
            if nt not in self.producciones:
                self.producciones[nt] = [] # Lista para el no terminal.
            self.producciones[nt].append(derivacion) #Derivacion al no terminal.

        # Calcular First, Follow y Select
        self.calcular_first()
        self.calcular_follow()
        self.calcular_select()

        # Mostrar la gramática con First, Follow y Select
        self.mostrar_gramatica()

    #Calcula first para cada no terminal.
    def calcular_first(self):
        self.en_proceso = set() #Control de simbolos para evitar bucles.
        for nt in self.producciones:
            self.first[nt] = self.obtener_first(nt) #Calcular first

    #Conjunto de first
    def obtener_first(self, simbolo):
        if simbolo.islower() or simbolo in ['+', '-', '*', '/', '(', ')']:
            return {simbolo} #Si es terminal, devuelve lo mismo. Habria que haber usado un diccionario.

        if simbolo == 'lambda':
            return {'lambda'}

        if simbolo in self.en_proceso:
            return set() #Evitar bucles por recursion directa o indirecta.

        self.en_proceso.add(simbolo) #Marca el simbolo como en proceso.
        first_set = set() #Inicializa el conjunto FIRST para el simbolo.

        #Recorre cada prodccion del simbolo para calcular su FIRST.
        for produccion in self.producciones[simbolo]:
            for sub_simbolo in produccion:
                sub_first = self.obtener_first(sub_simbolo) #Firsth simbolo siguiente.
                first_set.update(sub_first - {'lambda'}) #No deja lambda
                if 'lambda' not in sub_first:
                    break #Deja de agregar si no hay lambda
            else:
                first_set.add('lambda') #Si todos lo contienen, lo agrega.

        self.en_proceso.remove(simbolo) #Libera su estado en proceso.
        return first_set

    #Calcular follow.
    def calcular_follow(self):
        for nt in self.producciones:
            if nt not in self.follow:
                self.follow[nt] = set() #Conjunto follow vacio

        inicial = list(self.producciones.keys())[0] #Primer no terminal.
        self.follow[inicial].add('$') #Agregar $ fin de cadena.

        while True:
            actualizado = False #Controla si hubo cambios.

            for nt in self.producciones:
                for produccion in self.producciones[nt]:
                    for i, simbolo in enumerate(produccion):
                        if simbolo.isupper(): #Es un no terminal?.
                            siguiente_first = set()

                            if i + 1 < len(produccion):
                                siguiente_first = self.obtener_first(produccion[i + 1])
                                self.follow[simbolo].update(siguiente_first - {'lambda'}) #Agrega el follow.

                            if i + 1 == len(produccion) or 'lambda' in siguiente_first:
                                antes_actualizacion = len(self.follow[simbolo])
                                self.follow[simbolo].update(self.follow[nt]) #Propaga follow.
                                if antes_actualizacion != len(self.follow[simbolo]):
                                    actualizado = True #Actualizacion.

            if not actualizado:
                break #Si no existen mas actualizaciones.

    #Select de los conjuntos.
    def calcular_select(self):
        for nt in self.producciones:
            for produccion in self.producciones[nt]:
                select_set = set()

                first_produccion = self.obtener_first_string(produccion)

                if 'lambda' in first_produccion:
                    first_produccion.remove('lambda')
                    select_set.update(self.follow[nt]) #Agrego Follow si hay lambda.

                select_set.update(first_produccion) #Agrego first de la produccion.
                self.select[(nt, tuple(produccion))] = select_set #Guardo el select.

    #Conjunto FIRST para una secuencia de simbolos.
    def obtener_first_string(self, produccion):
        result = set()
        for simbolo in produccion:
            simbolo_first = self.obtener_first(simbolo)
            result.update(simbolo_first - {'lambda'}) #Agrega simbolos excepto lambda.
            if 'lambda' not in simbolo_first:
                break
        else:
            result.add('lambda') #La agrega si todos la tienen.
        return result

    #Impresion de cadena.
    def mostrar_gramatica(self):
        for nt in self.producciones:
            for produccion in self.producciones[nt]:
                # Calcular el First de esta producción en particular
                first = list(self.obtener_first_string(produccion))
                follow = list(self.follow[nt]) if nt in self.follow else []
                select = list(self.select.get((nt, tuple(produccion)), set()))
                print(f"{nt} : {' '.join(produccion)} {first} {follow} {select}")

    #Evaluar si pertenece a LL(1).
    def evaluar_cadena(self, cadena, limite_ciclos=1000):
        entrada = cadena.split() + ['$']  # Divide la cadena y agrega el símbolo de fin.
        pila = ['$']  # Inicializa la pila con el símbolo de fin.
        inicial = list(self.producciones.keys())[0]  # No terminal inicial.
        pila.append(inicial)

        i = 0  # Índice para recorrer la entrada.
        ciclos = 0  # Contador de ciclos.

        while pila:
            if ciclos >= limite_ciclos:
                print(f"Se ha alcanzado el límite de {limite_ciclos} ciclos. Posible bucle infinito.")
                return False  # Detenemos la evaluación por seguridad.

            ciclos += 1  # Incrementa el contador de ciclos.
            tope = pila.pop()  # Extrae el tope de la pila.

            if tope == entrada[i]:
                i += 1  # Avanza si coincide con la entrada.
            elif tope.isupper():  # Si es un no terminal.
                seleccion = None

                # Busca una producción válida en SELECT.
                for produccion in self.producciones[tope]:
                    if entrada[i] in self.select.get((tope, tuple(produccion)), set()):
                        seleccion = produccion
                        break

                if seleccion is not None:
                    for simbolo in reversed(seleccion):
                        if simbolo != 'lambda':
                            pila.append(simbolo)  # Agrega los símbolos a la pila.
                else:
                    return False  # Falla si no hay producción válida.
            else:
                return False  # Falla si no hay coincidencia.

        # Verificar si hemos llegado al final de la cadena de entrada y la pila está vacía
        if i == len(entrada) and not pila:
            return True
        else:
            return False

    #Verifica si es LL1 revisando conflictos.
    def es_ll1(self):
        for nt in self.producciones:
            select_sets = [self.select[(nt, tuple(prod))] for prod in self.producciones[nt]]
            combinados = set()  # Almacena símbolos únicos del SELECT.

            for s in select_sets:
                interseccion = combinados.intersection(s)
                if interseccion:
                    print(f"Conflicto en SELECT para '{nt}': {interseccion}")
                    return False  # Si hay conflicto, la gramática no es LL(1).
                combinados.update(s)

        return True  # Si no hay conflictos, es LL(1).