from typing import List, Optional
import sys
import random

GRID = List[List[str]]
ORIENTATION = tuple[int, int]
POSITION = tuple[int, int]

# --------------------------- READ WORDS -------------------------

def choose_words(filename: str, nwords: int, dim: int) -> set[int]:
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
    return chosen_words

# ------------------ GENERATE WORD SEARCH -------------------

def make_wordsearch(dim: int, words: set[str], complexity: int) -> Optional[GRID]:
    """
    Intenta generar una sopa de letras con la dimension, palabras y complexity
    dada. En caso de no ser posible, retorna una lista y un diccionario vacio.
    Si el conjunto de palabras es vacio, se retorna una sopa con la dimension pedida
    vacia. Por otro lado, si es posible generarse una sopa de letras, retornara
    una sopa de letras con las palabras ubicadas, y las demas posiciones vacias
    """
    wordsearch = [['_' for _ in range(dim)] for _ in range(dim)]

    orientations = direcciones_por_complejidad(complexity)

    # Si la complexity del juege fuese 3, entonces
    # se esta permitido que las palabras se intersequen
    cross_words = True if complexity == 3 else False

    # El stack lleva cuenta de las combinaciones que se prueban
    # en la sopa de letras
    stack = []
    positions = [(i, j) 
        for i in range(dim)
        for j in range(dim)
    ]

    unplaced_words = sorted(list(words), key = len)

    # Agregamos al stack el primer estado, el cual tiene
    # como sopa la sopa vacia, la palabra mas larga,
    # y una lista de todas las direcciones y posiciones a probar
    # para esta palabra
    stack.append(
        {
            "grid": wordsearch, 
            "word": words.pop(), 
            "positions": random.sample(positions, dim ** 2),
            "orientations": random.sample(list(orientations), len(orientations))
        }
    )

    while unplaced_words:
        # Si no hay mas estados para probar,
        # significa que no hay dispoisiciones posibles
        if not stack:
            return None

        current_state = stack[-1]

        # Comprobamos que haya posiciones en la sopa donde probar la palabra
        if current_state["positions"]:
            position = current_state["positions"][-1]
            # Comprobamos que haya direcciones para probar la palabra en la posicion
            if current_state["orientations"]:
                orientation = current_state["orientations"][-1]
                modified, wordsearch = modify_grid(
                    current_state["grid"], position, orientation, current_state["word"], cross_words
                )
                # Verificamos que se haya podido modificar la sopa y que no haya duplicados
                if modified and not check_duplicates(wordsearch, words):
                    # Si todavia hay palabras por colocar
                    # creamos un nuevo estado con la proxima palabra en la lista,
                    # inicializamos las posiciones y direcciones a probar, y agregamos el
                    # estado a la lista de estados
                    if unplaced_words:
                        new_state = {
                            "grid": wordsearch,
                            "word": unplaced_words.pop(),
                            "positions": random.sample(positions, dim ** 2),
                            "orientations": random.sample(list(orientations), len(orientations))
                        }
                        stack.append(new_state)
                else:
                    # Si la palabra no encajó en la sopa, quitamos la direccion
                    # para probar con la siguiente
                    current_state["orientations"].pop()
            else:
                # Al no haber direcciones para probar, probamos con la
                # siguiente posicion
                current_state["positions"].pop()
                current_state["orientations"] = random.sample(list(orientations), len(orientations))
        else:
            # Si no hay posiciones por probar, volvemos al estado anterior
            # y seguimos probando con distintas disposiciones
            stack.pop()
            # Restamos en uno el contador ya que ahora tenemos una
            # una palabra mas por colocar, y añadimos la palabra nuevamente a la
            # lista
            unplaced_words.append(current_state["word"])
    return wordsearch


def fill_wordsearch(grid: GRID, words: set[str]) -> GRID:
    """
    fill_wordsearch : Sopa Palabras -> Sopa
    Toma una lista de lista de strings (una sopa de letras) incompleta,
    donde faltan colocar caracteres que no van relacionados a las palabras,
    y rellena estos espacios tal que ninguna de las palabras a encontrar
    esté dos veces en la sopa
    """
    
    filled_wordsearch = fill_blanks(grid)

    while check_duplicates(filled_wordsearch, words):
        filled_wordsearch = fill_blanks(grid)

    return filled_wordsearch


def modify_grid(
    grid: GRID, position: POSITION, orientation: ORIENTATION, word: str, cross: bool
    ) -> tuple[bool, GRID]:
    """
    modify_grid: Sopa Tuple(Int, Int) Direccion Str Bool -> Tuple(Bool, Sopa)
    
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
    copy = copy_grid(grid)
    dim = len(grid)

    for i in range(len(word)):
        x = position[0] + orientation[0] * i
        y = position[1] + orientation[1] * i
        # Comprobamos que la posicion este dentro de la sopa
        if 0 <= x < dim and 0 <= y < dim:
            # Si la posicion no esta ocupada, o si se esta permitido
            # que las palabras se intersequen y el caracter a posicionar
            # es el mismo que se encuentra en la posicion, escribimos el
            # a la copia
            if grid[y][x] == '_' or (cross and word[i] == grid[y][x]):
                copy[y][x] = word[i]
                continue
        # Si no se ha podido modificar la sopa, retornamos
        # la sopa original
        return (False, grid)

    return (True, copy)


def check_duplicates(grid: GRID, words: set[str]) -> bool:
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
    words_counter = {word: 0 for word in words}
    # combinaciones es una lista de strings que almacenara
    # todas las filas columnas y diagonales de la sopa
    combinations = []
    combinations.extend(get_rows(grid))
    combinations.extend(get_cols(grid))
    combinations.extend(get_diagonals(grid))

    # Ordenamos las palabras por su longitud, de menor a mayor
    sorted_words = sorted(words, key = len)

    # Iteramos sobre las cadenas de caracteres que hay en la sopa
    for string in combinations:
        for word in sorted_words:
            # Si la palabra esta contenida en alguna de las cadenas
            # en la sopa (o la palabra al reves lo esta), aumentamos
            # en uno la cantidad de apariciones de dicha palabra en la sopa
            if word in string or word[::-1] in string:
                words_counter[word] += 1
                if words_counter[word] > 1:
                    return True
                break
    return False


# ---------------------- OBTENER COLUMNAS, FILAS Y DIAGONALES ------------------

def get_rows(grid: GRID) -> List[str]:
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
    return ["".join(row) for row in grid]


def get_cols(grid: GRID) -> List[str]:
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
    cols = []
    # Hacemos tantas repeticiones como columnas haya
    for i in range(len(grid)):
        col = ""
        # Por cada columna recorremos sobre las filas
        for j in range(len(grid)):
            # Añadimos el caracter al string col
            col += grid[j][i]
        # Añadimos el string que se forma a la lista de columnas
        cols.append(col)
    return cols


def get_diagonals(grid: GRID) -> List[str]:
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
    diagonals = []
    # Grid reversed horizontally to obtain the diagonals
    # of the matrix going in the other direction
    # [["a", "b"], ["c", "d"]] -> [["b", "a"], ["d", "c"]]
    flipped_grid = [row[::-1] for row in grid]
    dim = len(grid)

    # Agregamos las dos diagonales que
    # van de esquina a esquina
    # Main diagonals
    diag = ""
    flipped_diag = ""
    for i in range(dim):
        diag += grid[i][i]
        flipped_diag += flipped_grid[i][i]

    diagonals.append(diag)
    diagonals.append(flipped_diag)

    # Remaining diagonals
    for j in range(1, dim):
        
        # --- Diagonales de sentido arriba  ---
        # --- izquierda hacia abajo derecha ---
        
        # Diagonal que comienza desde arriba
        # desplazada j posiciones a la derecha
        diag_x = ""
        # Diagonal que comienza desde la izquierda
        # desplazada j posiciones hacia abajo
        diag_y = ""
        
        # --- Diagonales de sentido arriba  ---
        # --- derecha hacia abajo izquierda ---
        
        # Diagonal que comienza desde arriba
        # desplazada j posiciones hacia la izquierda
        flipped_diag_x = ""
        # Diagonal que comienza desde la derecha
        # desplazada j posiciones hacia abajo
        flipped_diag_y = ""

        for i in range(dim - j):
            diag_x += grid[i][j+i]
            diag_y += grid[j+i][i]
            flipped_diag_x += flipped_grid[i][j+i]
            flipped_diag_y += flipped_grid[j+i][i]

        diagonals.extend((diag_x, diag_y, flipped_diag_x, flipped_diag_y))

    return diagonals


# ------------------------ FUNCIONES AUXILIARES SOPA ----------------

def direcciones_por_complejidad(complexity: int) -> set[ORIENTATION]:
    """
    direcciones_por_complejidad: Int -> Set(Direccion)
    
    Recibe el nivel de complexity del juego y devuelve un
    conjunto de tuplas las cuales representan las direcciones
    en las cuales pueden estar dispuestas las palabras
    """
    orientations = {(1,0), (0,1)}
    if complexity >= 1:
        orientations.add((1,1))
        if complexity > 1:    
            orientations.update([(-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)])
    return orientations


def fill_blanks(grid: GRID) -> GRID:
    """
    fill_blanks: Sopa -> Sopa
    Toma una sopa y completa todos los espacios
    que esten vacios (se considera vacio si hay un "_" en
    dicha posicion) con alguna letra aleatoria
    """
    copy = copy_grid(grid)
    dim = len(grid)

    # Iteramos sobre filas y columnas
    for i in range(dim):
        for j in range(dim):
            # Si en la posicion actual la sopa no esta
            # vacia, continuamos
            if grid[i][j] != '_':
                continue
            # Sino, la completamos con una letra aleatoria
            letter = chr(random.randint(ord("a"), ord("z")))
            copy[i][j] = letter

    return copy


def print_wordsearch(wordsearch: GRID, words: set[str]) -> None:
    """
    print_wordsearch: Sopa -> None
    Toma una sopa y la imprime a la terminal
    """
    print("\nWORDSEARCH")
    print("Words to search: ")
    for word in words:
        print(f"- {word}")
    print()
    for row in wordsearch:
        print(" ".join(row))
    print()


def copy_grid(grid: GRID) -> GRID:
    """
    copy_grid: Sopa -> Sopa
    Toma una sopa y retorna una copia, para poder
    modificar la copia sin modificar la original
    """
    copy = []
    # Iteramos sobre las filas
    for row in grid:
        # Agregamos a copia una copia de la fila
        copy.append(row[:])
    return copy


# ------------------------- FUNCION PRINCIPAL -----------------------

def main() -> None:
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
    filename, nwords, dim, complexity = args
    nwords, dim, complexity = int(nwords), int(dim), int(complexity)

    # Randomly choose words that fit
    words = choose_words(filename, nwords, dim)

    # We generate a grid with the required conditions
    grid = make_wordsearch(dim, words, complexity)
    if grid is None:
        raise ValueError("Could not generate a wordsearch with the asked conditions")

    # Fill the wordsearch without creating duplicates
    wordsearch = fill_wordsearch(grid, words)

    print_wordsearch(wordsearch, words)


if __name__ == "__main__":
    main()