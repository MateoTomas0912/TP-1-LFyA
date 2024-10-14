# Integrantes:
* Abarca Vecchio, Juan Ignacio
* Tomas, Mateo
* Rolheiser, Eric

# Detalles del trabajo practico:

Desarrollar un programa que cree un parser LL (1) a partir de una gramática dada por el usuario, con el fin de verificar si una cadena forma parte del lenguaje que define dicha gramática. Implementar la clase “Gramatica” en Python que tenga los siguientes métodos:

1) setear(string)
Esta función debe implementar la lógica suficiente para que al imprimir en pantalla una instancia de este objeto a la que se le haya invocado dicho método previamente se muestre la gramática de la siguiente manera: por cada regla o producción mostrar dicha regla y a continuación los First, Follows y Selects correspondientes. Además, este objeto, debe poseer un campo EsLL1 de tipo bool, indicando si la gramática puede reconocerse o no mediante esta técnica.

2) evaluar_cadena(string)
Devuelve true en caso de que la cadena se derive de la gramática y false en caso contrario. 

Para el módulo mencionado previamente, implementar sus correspondientes test para validar el correcto funcionamiento del mismo. Dichos test deben incluir al menos:
Una gramática LL(1) sin recursión a derecha
Una gramática LL(1) con recursión a derecha
Una gramática LL(1) que incluya lambda en sus derivaciones
Una gramática LL(1) que no incluya lambda en sus derivaciones
Una gramática LL(1) con reglas de producción innecesarias.
Una gramática LL(1) con símbolos inaccesibles desde el axioma.
Una gramática LL(1) con no terminales no generativos.
Por cada uno de los incisos previos, una gramática que no sea LL(1).
Una gramática no LL(1) con recursión a izquierda

## Consideraciones:
Debe ser capaz de detectar y resolver reglas de producción innecesarias, símbolos inaccesibles desde el axioma y no terminales no generativos.
Se considera no terminal a cualquier palabra que comienza con letra mayúscula.
Terminales y no terminales pueden contener más de una letra.
El símbolo “:” y la palabra “lambda” son reservadas.
La antecedente de la primera regla de la gramática es el no terminal distinguido.
Las producciones se separan con \n, el antecedente del consecuente con “:” y los elementos del consecuente con espacio/s.
