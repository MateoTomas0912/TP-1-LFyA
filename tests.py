from tpLFA import Gramatica

#Ejecutador de TEST.
def ejecutar_pruebas(gramatica, pruebas, limite_ciclos=1000):
    gramatica.es_ll1()  # Verifica si es LL(1).

    for cadena, esperado in pruebas:
        resultado = gramatica.evaluar_cadena(cadena, limite_ciclos=limite_ciclos)
        print(f"Cadena: '{cadena}' - Resultado: {resultado} - Esperado: {esperado}")
    print('')


#TEST's
#TEST's LL(1)
def test_1_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A
    A : a B
    B : b
    """)
    ejecutar_pruebas(gramatica, [("a b", True), ("a", False), ("b", False)])

def test_2_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    E : T E'
    E' : + T E'
    E' : lambda
    T : F T'
    T' : * F T'
    T' : lambda
    F : ( E )
    F : num
    """)
    ejecutar_pruebas(gramatica, [("num + num", True), ("num + num * num", True), ("num + * num", False)])

def test_3_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    A : a
    A : lambda
    B : b
    """)
    ejecutar_pruebas(gramatica, [("a b", True), ("b", True), ("a", False)])

def test_4_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : a A b
    A : c
    """)
    ejecutar_pruebas(gramatica, [("a c b", True), ("a b", False)])

def test_5_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B C
    A : a
    A : d
    B : b
    C : c
    D : e
    """)
    #D : e   Regla innecesaria
    ejecutar_pruebas(gramatica, [("a b c", True), ("d b c", True), ("a d c", False), ("b c", False)])

def test_6_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : a A
    A : b
    B : c
    """)
    #B: c
    ejecutar_pruebas(gramatica, [("a b", True), ("c", False)])

def test_7_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : a A
    A : B
    B : lambda
    """)
    ejecutar_pruebas(gramatica, [("a", True), ("a b", False)])

#TEST's no LL(1)
def test_1_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    S : a C D 
    A : a A
    A : a
    B : b B
    B : lambda
    C : c C
    C : d
    D : e
    """)
    # Conflicto: S puede comenzar con 'a' o con A.
    ejecutar_pruebas(gramatica, [("a b", True), ("a a", True), ("c d", True), ("b", False)])

def test_2_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : a S
    S : b T
    T : c T
    T : d
    T : lambda
    """)
    # Conflicto: ambas producciones pueden comenzar con 'a' o 'b'.
    # Esto introduce ambigüedad adicional.
    ejecutar_pruebas(gramatica, [("a c", True), ("b d", True), ("a b", True), ("a", False)])

def test_3_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    A : a A
    A : lambda
    B : b C
    C : c C
    C : d
    """)
    # Conflicto: A puede derivar en 'a' o ser vacío.
    ejecutar_pruebas(gramatica, [("a b c", True), ("a d", True), ("b", False), ("", True)])

def test_4_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    A : a A
    A : b
    B : b C
    C : c C
    C : d
    """)
    # Conflicto: ambas producciones comienzan con 'a' o 'b'.
    ejecutar_pruebas(gramatica, [("a b", True), ("b c", True), ("b d", True), ("a", False)])

def test_5_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    A : a A
    A : b
    B : b C
    C : d
    D : e
    """)
    # Conflicto: ambas producciones comienzan con 'a' o 'b'.
    # Regla innecesaria pero introduce ambigüedad. C.
    ejecutar_pruebas(gramatica, [("a b", True), ("b b", True), ("b d", False), ("a a b", True)])

def test_6_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : A B
    A : a A
    A : b
    B : c D
    D : d
    E : e
    """)
    # 'b' es inaccesible pero puede generar ambigüedad.
    # Inaccesible desde S. 'e'.
    ejecutar_pruebas(gramatica, [("a b", True), ("b d", True), ("c d", False), ("b", False)])

def test_7_no_ll1():
    gramatica = Gramatica()
    gramatica.setear("""
    S : W Q
    S : a S b
    S : W
    S : R
    W : a W Q
    W : a
    Q : Q b
    Q : lambda
    R : R b
    """)
    ejecutar_pruebas(gramatica, [("aabb", True), ("a", True), ("ab", False), ("b", False), ("a b", False)])

#TEST recursion izquierda
def test_1_recursion_izq():
    gramatica = Gramatica()
    gramatica.setear("""
    S : S a
    S : b
    """)
    ejecutar_pruebas(gramatica, [("b", True), ("b a", True), ("a", False)], limite_ciclos=50)

#Main con los tests
def main():
    # Tests LL(1)
    test_1_ll1()
    test_2_ll1()
    test_3_ll1()
    test_4_ll1()
    test_5_ll1()
    test_6_ll1()
    test_7_ll1()

    # Tests no LL(1)
    test_1_no_ll1()
    test_2_no_ll1()
    test_3_no_ll1()
    test_4_no_ll1()
    test_5_no_ll1()
    test_6_no_ll1()
    test_7_no_ll1()

    # Test no LL(1) recursion a izq
    test_1_recursion_izq()

if __name__ == "__main__":
    main()