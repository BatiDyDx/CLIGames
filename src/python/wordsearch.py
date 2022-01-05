from typing import List
import sys
import random

"""
Definimos los siguientes tipos para facilitar la lectura de
las signaturas de las funciones

Sopa: List(List(Str))
Palabras: Set(Str)
Direccion: Tuple(Int, Int)
"""

# --------------------------- READ WORDS -------------------------

def choose_words(filename: str, nwords: int, dim: int) -> List[int]:
    with open(filename) as f:
        words: List[str] = f.readlines()
        words_in_file: int = len(words)
    chosen_words = set()
    while len(chosen_words) < nwords:
        random_line: int = random.randrange(0, words_in_file)
        random_word: str = words[random_line].strip().lower()
        if len(random_word) > dim:
            continue
        chosen_words.add(random_word)
    return list(chosen_words)

# ------------------ FUNCIONES GENERAR SOPA DE LETRAS -------------------

def generar_sopa(dim, palabras, complejidad):
    """
    generar_sopa : Int Palabras Int -> Sopa
    Intenta generar una sopa de letras con la dimension, palabras y complejidad
    dada. En caso de no ser posible, retorna una lista y un diccionario vacio.
    Si el conjunto de palabras es vacio, se retorna una sopa con la dimension pedida
    vacia. Por otro lado, si es posible generarse una sopa de letras, retornara
    una sopa de letras con las palabras ubicadas, y las demas posiciones vacias
    """
    sopa = [['_' for _ in range(dim)] for _ in range(dim)]

    if not palabras:
        return sopa
    
    direcciones = direcciones_por_complejidad(complejidad)

    # Si la complejidad del juege fuese 3, entonces
    # se esta permitido que las palabras se intersequen
    intersecar_palabras = True if complejidad == 3 else False

    # El stack lleva cuenta de las combinaciones que se prueban
    # en la sopa de letras
    stack = []
    posiciones = []

    for i in range(dim):
        for j in range(dim):
            posiciones.append((i ,j))

    palabras_sin_colocar = sorted(list(palabras), key = len)

    # Agregamos al stack el primer estado, el cual tiene
    # como sopa la sopa vacia, la palabra mas larga,
    # y una lista de todas las direcciones y posiciones a probar
    # para esta palabra
    stack.append(
        {
            "sopa": sopa, 
            "palabra": palabras.pop(), 
            "posiciones": random.sample(posiciones, dim ** 2),
            "direcciones": random.sample(list(direcciones), len(direcciones))
        }
    )

    while palabras_sin_colocar:
        # Si no hay mas estados para probar,
        # significa que no hay dispoisiciones posibles
        if not stack:
            return list()

        estado_actual = stack[-1]

        # Comprobamos que haya posiciones en la sopa donde probar la palabra
        if estado_actual["posiciones"]:
            posicion = estado_actual["posiciones"][-1]
            # Comprobamos que haya direcciones para probar la palabra en la posicion
            if estado_actual["direcciones"]:
                direccion = estado_actual["direcciones"][-1]
                modificado, sopa = modificar_sopa(
                        estado_actual["sopa"], posicion, direccion, estado_actual["palabra"], intersecar_palabras
                )
                # Verificamos que se haya podido modificar la sopa y que no haya duplicados
                if modificado and not hay_duplicados(sopa, palabras):
                    # Si todavia hay palabras por colocar
                    # creamos un nuevo estado con la proxima palabra en la lista,
                    # inicializamos las posiciones y direcciones a probar, y agregamos el
                    # estado a la lista de estados
                    if palabras_sin_colocar:
                        nuevo_estado = {
                            "sopa": sopa,
                            "palabra": palabras_sin_colocar.pop(),
                            "posiciones": random.sample(posiciones, dim ** 2),
                            "direcciones": random.sample(list(direcciones), len(direcciones))
                        }
                        stack.append(nuevo_estado)
                else:
                    # Si la palabra no encajó en la sopa, quitamos la direccion
                    # para probar con la siguiente
                    estado_actual["direcciones"].pop()
            else:
                # Al no haber direcciones para probar, probamos con la
                # siguiente posicion
                estado_actual["posiciones"].pop()
                estado_actual["direcciones"] = random.sample(list(direcciones), len(direcciones))
        else:
            # Si no hay posiciones por probar, volvemos al estado anterior
            # y seguimos probando con distintas disposiciones
            stack.pop()
            # Restamos en uno el contador ya que ahora tenemos una
            # una palabra mas por colocar, y añadimos la palabra nuevamente a la
            # lista
            palabras_sin_colocar.append(estado_actual["palabra"])
    return sopa


def completar_sopa(sopa, palabras):
    """
    completar_sopa : Sopa Palabras -> Sopa
    Toma una lista de lista de strings (una sopa de letras) incompleta,
    donde faltan colocar caracteres que no van relacionados a las palabras,
    y rellena estos espacios tal que ninguna de las palabras a encontrar
    esté dos veces en la sopa
    """
    
    dim = len(sopa)

    sopa_completada = completar_espacios(sopa)

    while hay_duplicados(sopa_completada, palabras):
        sopa_completada = completar_espacios(sopa)

    return sopa_completada


def modificar_sopa(sopa, pos, dir, palabra, intersecar_palabras):
    """
    modificar_sopa: Sopa Tuple(Int, Int) Direccion Str Bool -> Tuple(Bool, Sopa)
    
    Toma una sopa, una posicion, direccion y palabra, y un booleano que indica la posibilidad de
    que las palabras se intersequen en la sopa. Se intenta colocar la palabra dada
    en la sopa iniciando en la posicion y en la direccion dada. Si se puede,
    retorna una tupla con un True, y la nueva sopa. Si no se puede insertar la palabra,
    retorna una tupla con un primer elemento False y la sopa original.

    Ejemplo:
    
    Entrada:
    [["t", "e", "l", "a"], 
    ["_", "e", "_", "_"],
    ["d", "_", "_", "_"],
    ["_", "_", "_", "_"]],
    (3, 0), (0, 1), "agua", True)

    Salida:
    (True, [["t", "e", "l", "a"],
            ["_", "e", "_", "g"],
            ["d", "_", "_", "u"],
            ["_", "_", "_", "a"]])

    """
    # Creamos una copia para no modificar la original
    copia = copiar_sopa(sopa)
    dim = len(sopa)

    for i in range(len(palabra)):
        x = pos[0] + dir[0] * i
        y = pos[1] + dir[1] * i
        # Comprobamos que la posicion este dentro de la sopa
        if 0 <= x < dim and 0 <= y < dim:
            # Si la posicion no esta ocupada, o si se esta permitido
            # que las palabras se intersequen y el caracter a posicionar
            # es el mismo que se encuentra en la posicion, escribimos el
            # a la copia
            if sopa[y][x] == '_' or (intersecar_palabras and palabra[i] == sopa[y][x]):
                copia[y][x] = palabra[i]
                continue
        # Si no se ha podido modificar la sopa, retornamos
        # la sopa original
        return (False, sopa)

    return (True, copia)


def hay_duplicados(sopa, palabras):
    """
    hay_duplicados : Sopa Palabras -> Bool

    Retorna True si algunas de las palabras en el conjunto de
    palabras aparece repetida en la sopa de letras, y False
    si ninguna de las palabras esta repetida

    Ejemplos:
    >>> hay_duplicados([
                ["t", "e", "l", "a"], 
                ["r", "e", "n", "g"],
                ["d", "m", "l", "u"],
                ["e", "o", "a", "a"]], 
                {"del", "agua", "tela"}
    )
    True
    """
    contador_palabras = {palabra: 0 for palabra in palabras}
    # combinaciones es una lista de strings que almacenara
    # todas las filas columnas y diagonales de la sopa
    combinaciones = []
    combinaciones.extend(obtener_filas(sopa))
    combinaciones.extend(obtener_columnas(sopa))
    combinaciones.extend(obtener_diagonales(sopa))

    # Ordenamos las palabras por su longitud, de menor a mayor
    palabras_ordenadas = sorted(palabras, key = len)

    # Iteramos sobre las cadenas de caracteres que hay en la sopa
    for cadena in combinaciones:
        for palabra in palabras_ordenadas:
            # Si la palabra esta contenida en alguna de las cadenas
            # en la sopa (o la palabra al reves lo esta), aumentamos
            # en uno la cantidad de apariciones de dicha palabra en la sopa
            if palabra in cadena or palabra[::-1] in cadena:
                contador_palabras[palabra] += 1
                break
    palabra_esta_repetida = lambda palabra: contador_palabras[palabra] > 1
    # Obtenemos un conjunto de las palabras que aparezcan mas de una vez en
    # la sopa (osea las palabras que estan repetidas)
    palabras_repetidas = set(filter(palabra_esta_repetida, palabras))
    # Si hay algun elemento en el conjunto, entonces es porque hay repeticiones,
    # de lo contrario no hay repeticiones
    return len(palabras_repetidas) > 0


# ---------------------- OBTENER COLUMNAS, FILAS Y DIAGONALES ------------------

def obtener_filas(sopa):
    """
    obtener_fila: Sopa -> List(Str)
    
    Retorna una lista de strings que se forman a lo largo
    de todas las filas de la sopa
    
    Ejemplos:
    >>> obtener_columna([["a", "b"], ["c", "d"]])
    ["ab", "cd"]
    >>> obtener_diagonal([["s", "o", "l"], ["d", "o", "s"], ["l", "a", "s"]])
    ["sol", "dos", "las"]
    """
    # Para cada fila en la sopa, juntamos los caracteres
    # y asi obtenemos el string a lo largo de la fila
    filas = ["".join(fila) for fila in sopa]
    return filas


def obtener_columnas(sopa):
    """
    obtener_columnas: Sopa -> List(Str)
    Retorna la lista de strings que se forman en las
    columnas de la sopa
    Ejemplos:
    >>> obtener_columna([["a", "b"], ["c", "d"]])
    ["ac", "bd"]
    >>> obtener_diagonal([["s", "o", "l"], ["d", "o", "s"], ["l", "a", "s"]]) 
    ["sdl", "ooa", "lss"]
    """
    columnas = []
    # Hacemos tantas repeticiones como columnas haya
    for i in range(len(sopa)):
        col = ""
        # Por cada columna recorremos sobre las filas
        for j in range(len(sopa)):
            # Añadimos el caracter al string col
            col += sopa[j][i]
        # Añadimos el string que se forma a la lista de columnas
        columnas.append(col)
    return columnas


def obtener_diagonales(sopa):
    """
    obtener_diagonal: Sopa -> List(Str)
    Retorna una lista de strings que se forman a lo largo
    de todas las diagonales de la sopa (tanto las diagonales
    de sentido arriba izquierda hacia abajo derecha como las
    diagonales de sentido arriba derecha hacia abajo izquierda)
    Ejemplos:
    >>> obtener_diagonales([["a", "b"], ["c", "d"]])
    ["ad", "b", "c", "bc", "d", "a"]
    """
    diagonales = []
    sopa_inv = [fila[::-1] for fila in sopa]
    dim = len(sopa)

    # Agregamos las dos diagonales que
    # van de esquina a esquina
    diagonal = ""
    diagonal_inv = ""
    for i in range(dim):
        diagonal += sopa[i][i]
        diagonal_inv += sopa_inv[i][i]

    diagonales.append(diagonal)
    diagonales.append(diagonal_inv)

    # Agregamos las demas diagonales
    for j in range(1, dim):
        
        # --- Diagonales de sentido arriba  ---
        # --- izquierda hacia abajo derecha ---
        
        # Diagonal que comienza desde arriba
        # desplazada j posiciones a la derecha
        diagonal_x = ""
        # Diagonal que comienza desde la izquierda
        # desplazada j posiciones hacia abajo
        diagonal_y = ""
        
        # --- Diagonales de sentido arriba  ---
        # --- derecha hacia abajo izquierda ---
        
        # Diagonal que comienza desde arriba
        # desplazada j posiciones hacia la izquierda
        diagonal_inv_x = ""
        # Diagonal que comienza desde la derecha
        # desplazada j posiciones hacia abajo
        diagonal_inv_y = ""

        for i in range(dim - j):
            diagonal_x += sopa[i][j+i]
            diagonal_y += sopa[j+i][i]
            diagonal_inv_x += sopa_inv[i][j+i]
            diagonal_inv_y += sopa_inv[j+i][i]

        diagonales.extend((diagonal_x, diagonal_y, diagonal_inv_x, diagonal_inv_y))

    return diagonales


# ------------------------ FUNCIONES AUXILIARES SOPA ----------------

def direcciones_por_complejidad(complejidad):
    """
    direcciones_por_complejidad: Int -> Set(Direccion)
    
    Recibe el nivel de complejidad del juego y devuelve un
    conjunto de tuplas las cuales representan las direcciones
    en las cuales pueden estar dispuestas las palabras
    """
    direcciones = {(1,0), (0,1)}
    if complejidad >= 1:
        direcciones.add((1,1))
        if complejidad > 1:    
            direcciones.update([(-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)])
    return direcciones


def validar_palabras(dim, palabras, complejidad):
    """
    validar_palabras: Int Palabras Int -> None
    La funcion corre algunos casos de prueba iniciales para
    ver si es posible armar una sopa de letras con las palabras
    y dimension dadas. Esto es para descartar desde el comienzo
    algunos casos donde no es posible armar la sopa de letras, por
    lo que el hecho de que la funcion no levante un error no
    nos asegura que vaya a ser posible el armado de la sopa
    """
    cant_caracteres = 0
    for palabra in palabras:
        # Si la longitud de la palabra es mayor a la dimension
        # de la sopa, entonces no es posible insertar la palabra
        if len(palabra) > dim:
            error = "No es posible insertar una palabra de " + str(len(palabra))
            error +=  " caracteres en una sopa de dimension " + str(dim)
            raise ValueError(error)
        cant_caracteres += len(palabra)
    # En el caso en que las palabras no se puedan superponer (si complejidad < 3)
    # la suma de todas las letras de las palabras no puede ser mayor
    # a la cantidad de casillas de la sopa
    if cant_caracteres > dim ** 2 and complejidad < 3:
        error = "No se puede generar una sopa de letras con " + str(cant_caracteres) 
        error += " caracteres y " + str((dim ** 2)) + " casillas"
        raise ValueError(error)
    return


def completar_espacios(sopa):
    """
    completar_espacios: Sopa -> Sopa
    Toma una sopa y completa todos los espacios
    que esten vacios (se considera vacio si hay un "_" en
    dicha posicion) con alguna letra aleatoria
    """
    copia = copiar_sopa(sopa)
    dim = len(sopa)

    # Iteramos sobre filas y columnas
    for i in range(dim):
        for j in range(dim):
            # Si en la posicion actual la sopa no esta
            # vacia, continuamos
            if sopa[i][j] != '_':
                continue
            # Sino, la completamos con una letra aleatoria
            letra = chr(random.randint(ord("a"), ord("z")))
            copia[i][j] = letra

    return copia


def imprimir_sopa(sopa):
    """
    imprimir_sopa: Sopa -> None
    Toma una sopa y la imprime a la terminal
    """
    print()
    for fila in sopa:
        print(" ".join(fila))
    print()


def copiar_sopa(sopa):
    """
    copiar_sopa: Sopa -> Sopa
    Toma una sopa y retorna una copia, para poder
    modificar la copia sin modificar la original
    """
    copia = []
    # Iteramos sobre las filas
    for fila in sopa:
        # Agregamos a copia una copia de la fila
        copia.append(fila[:])
    return copia


# ------------------------- FUNCION PRINCIPAL -----------------------

def main():
    """
    main: None -> None

    Parsea el archivo descripcion con la informacion de
    la sopa de letras, crea una sopa de letras con dichas
    condiciones y la imprime a la terminal
    """
    if len(sys.argv) != 5:
        print(
            "Usage: python " + sys.argv[0] + " <words_filename> <words_number> <grid_dimension> <game_complexity>"
        )
        return

    args = sys.argv[1:]
    filename, nwords, dim, cplex = args
    nwords, dim, cplex = int(nwords), int(dim), int(cplex)

    words = choose_words(filename, nwords, dim)

    # Intentamos descartar casos donde no es posible
    # armar una sopa de letras
    validar_palabras(dim, words, cplex)

    # Generamos una lista con las condiciones requeridas
    sopa_incompleta = generar_sopa(dim, words, cplex)
    if sopa_incompleta == list():
        raise ValueError("No se pudo generar una sopa de letras con las condiciones pedidas")

    # Completamos la sopa asegurandonos que no se generen
    # palabras duplicadas
    sopa = completar_sopa(sopa_incompleta, words)

    # Escribimos la salida a la terminal
    print("Sopa De Letras")
    imprimir_sopa(sopa)


if __name__ == "__main__":
    main()