import os
import time

class TuringMachine:
    def __init__(self):
        self.cinta1 = []
        self.cinta2 = []
    
    def imprimir_cintas(self):
        print("Contenido de la Cinta 1:", ''.join(self.cinta1))
        print("Contenido de la Cinta 2:", ''.join(self.cinta2))

    def procesar_input(self, input_string):
        for i, char in enumerate(input_string):
            if i % 2 == 0:
                self.cinta1.append(char)  # Caracter en la cinta 1
            else:
                self.cinta2.append(char)  # Caracter en la cinta 2
        self.imprimir_cintas()
        
    
    

class Automata: 
    def __init__(self):
        # Definir los estados y el estado inicial
        self.states = {'q0': 0, 'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4, 'q5': 5, 'q6': 6}
        self.current_state = 'q0'
        self.final_states = ['q6']  # Estados finales

        # Definir las transiciones del autómata
        self.transitions = {
            ('q0', 'a'): 'q1',
            ('q1', 'b'): 'q2',
            ('q2', 'a'): 'q3',
            ('q3', 'a'): 'q1',
            ('q3', 'b'): 'q4',
            ('q4', '#'): 'q5',
            ('q5', 'a'): 'q5',
            ('q5', 'b'): 'q5',
            ('q5', '*'): 'q6',
        }

        self.transition_log = []  # Almacena las transiciones

    def reset(self):
        """Reiniciar el autómata al estado inicial."""
        self.current_state = 'q0'
        self.transition_log.clear()

    def transition(self, symbol):
        """Realizar una transición dado un símbolo."""
        try:
            new_state = self.transitions[(self.current_state, symbol)]
            self.transition_log.append((self.current_state, symbol, new_state))
            self.current_state = new_state
        except KeyError:
            self.current_state = None  # Transición inválida

    def is_valid(self):
        """Comprobar si el estado actual es válido (estado final)."""
        return self.current_state in self.final_states

    def process_string(self, input_string):
        """Procesar una cadena a través del autómata."""
        self.reset()
        for symbol in input_string:
            self.transition(symbol)
        return self.is_valid()

    def get_transition_log(self):
        """Devolver el registro de transiciones."""
        return self.transition_log

    def build_derivation_tree(self, input_string):
        """Construir el árbol de derivación (simplificado) para una cadena."""
        tree = []
        for symbol in input_string:
            tree.append(f"{self.current_state} --({symbol})--> {self.transitions.get((self.current_state, symbol), 'None')}")
            self.transition(symbol)
        return tree

    def build_derivation_table(self, input_string):
        """Construir la tabla de derivación (simplificada)."""
        table = []
        for symbol in input_string:
            current = self.current_state
            new_state = self.transitions.get((current, symbol), 'None')
            table.append([current, symbol, new_state])
            self.transition(symbol)
        return table

    def simulate_stack(self, input_string):
        """Simular una pila que difunde los caracteres de la cadena."""
        stack = []
        for symbol in input_string:
            # Push al carácter en la pila
            stack.append(symbol)
            print(f"Push: {symbol}, Pila: {stack}")

            # Pop del carácter de la pila cuando se procesa
            stack.pop()
            print(f"Pop: {symbol}, Pila: {stack}")


def read_strings_from_file(file_path):
    """Leer cadenas desde un archivo .txt."""
    with open(file_path, 'r') as file:
        strings = file.read().splitlines()
    return strings

def clear_console():
    """Limpiar la consola."""
    # Comando para limpiar la consola dependiendo del sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def process_strings(file_path):
    """Procesar cadenas del archivo, construir árbol, tabla, pila, y mostrar un resumen."""
    automata = Automata()
    valid_strings = []
    invalid_strings = []

    # Leer cadenas desde el archivo
    strings = read_strings_from_file(file_path)

    # Procesar cada cadena
    for string in strings:
        clear_console()  # Limpiar la consola antes de mostrar cada cadena
        print(f"\nProcesando cadena: {string}")

        # Árbol de derivación
        automata.reset()  # Reiniciar el autómata antes de procesar cada cadena
        derivation_tree = automata.build_derivation_tree(string)
        print("Árbol de derivación:")
        for step in derivation_tree:
            print(step)

        # Tabla de derivación
        automata.reset()
        derivation_table = automata.build_derivation_table(string)
        print("Tabla de derivación:")
        for row in derivation_table:
            print(row)

        # Simulación de la pila
        automata.reset()
        print("Simulación de la pila:")
        automata.simulate_stack(string)

        # Validación de la cadena
        automata.reset()
        if automata.process_string(string):
            valid_strings.append(string)
            print(f"Cadena válida: {string}")
        else:
            invalid_strings.append(string)
            print(f"Cadena inválida: {string}")

        Turing = TuringMachine()

        Turing.procesar_input(string)


        # Espera a que el usuario presione "Enter" antes de continuar
        input("\nPresiona 'Enter' para continuar a la siguiente cadena...")
        # Añadir una pequeña pausa antes de limpiar, si es necesario
        time.sleep(0.5)

    # Mostrar resumen final al procesar todas las cadenas
    clear_console()
    print("\nResumen final:")
    print(f"Cadenas válidas ({len(valid_strings)}): {valid_strings}")
    print(f"Cadenas inválidas ({len(invalid_strings)}): {invalid_strings}")

# Ejecución del procesamiento de cadenas
file_path = r"C:\Users\adria\OneDrive\Documents\Pruebas\LFA\automaton_strings.txt"  # Cambia esta ruta si es necesario
process_strings(file_path)
