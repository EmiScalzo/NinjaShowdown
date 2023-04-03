import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random
import os
import openpyxl

# Cargamos los datos de los personajes desde el archivo "personajes.xlsx"
df_personajes = pd.read_excel("personajes.xlsx")

# Cargamos los datos de las habilidades desde el archivo "habilidades.xlsx"
df_habilidades = pd.read_excel("habilidades.xlsx")

# Función para cargar los datos de los personajes desde un archivo Excel
def cargar_personajes():
    # Abre un cuadro de diálogo para seleccionar el archivo Excel
    filename = filedialog.askopenfilename(initialdir="./", title="Seleccionar archivo", filetypes=(("Archivos de Excel", "*.xlsx"),))
    
    # Lee el archivo Excel y lo convierte en un DataFrame de Pandas
    df = pd.read_excel(filename)
    
    # Actualiza el DataFrame con los datos de los personajes
    df_personajes = df.copy()

    # Actualiza la lista de personajes en la GUI
    listbox.delete(0, tk.END)
    for index, row in df_personajes.iterrows():
        listbox.insert(tk.END, row["Nombre"])

# Función para cargar los datos de las habilidades desde un archivo Excel
def cargar_habilidades():
    # Abre un cuadro de diálogo para seleccionar el archivo Excel
    filename = filedialog.askopenfilename(initialdir="./", title="Seleccionar archivo", filetypes=(("Archivos de Excel", "*.xlsx"),))
    
    # Lee el archivo Excel y lo convierte en un DataFrame de Pandas
    df = pd.read_excel(filename)
    
    # Actualiza el DataFrame con los datos de las habilidades
    df_habilidades = df.copy()

    # Actualiza la lista de habilidades en la GUI
    listbox.delete(0, tk.END)
    for index, row in df_habilidades.iterrows():
        listbox.insert(tk.END, row["Nombre"])

# Función para crear la GUI
def crear_gui():
    # Crea una ventana
    ventana = tk.Tk()
    ventana.title("Simulador de peleas de Naruto")
    
    # Crea una lista para mostrar los personajes y habilidades
    listbox = tk.Listbox(ventana)
    listbox.pack(padx=10, pady=10)

    # Agrega los personajes a la lista
    for index, row in df_personajes.iterrows():
        listbox.insert(tk.END, row["Nombre"])

    # Agrega las habilidades a la lista
    for index, row in df_habilidades.iterrows():
        listbox.insert(tk.END, row["Nombre"])

    # Crea dos botones para cargar los datos de los personajes y las habilidades
    cargar_personajes_btn = tk.Button(ventana, text="Cargar datos de personajes", command=cargar_personajes)
    cargar_personajes_btn.pack(pady=10)
    
    cargar_habilidades_btn = tk.Button(ventana, text="Cargar datos de habilidades", command=cargar_habilidades)
    cargar_habilidades_btn.pack(pady=10)
    
    # Inicia el bucle de la ventana
    ventana.mainloop()

# Llama a la función para crear la GUI
crear_gui()


class HabilidadesFrame(tk.Frame):
    def __init__(self, master, personaje):
        super().__init__(master)

        self.personaje = personaje
        self.habilidades = self.cargar_habilidades()

        self.habilidades_var = {}
        self.habilidades_costo = {}
        self.cargar_habilidades_var()

        tk.Label(self, text=f"Seleccione las habilidades de {self.personaje['Nombre']}").pack(pady=5)

        for habilidad, costo in self.habilidades_costo.items():
            tk.Label(self, text=f"{habilidad} ({costo} chakra)").pack(anchor="w")
            tk.Checkbutton(self, variable=self.habilidades_var[habilidad]).pack(anchor="w")

        tk.Button(self, text="Simular pelea", command=self.simular_pelea).pack(pady=10)

    def cargar_habilidades(self):
        habilidades = {}

        workbook = openpyxl.load_workbook(filename='habilidades.xlsx')
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            habilidades[row[0]] = int(row[1])

        return habilidades

    def cargar_habilidades_var(self):
        for habilidad in self.habilidades:
            self.habilidades_var[habilidad] = tk.BooleanVar(value=False)
            self.habilidades_costo[habilidad] = self.habilidades[habilidad]

    def simular_pelea(self):
        habilidades_seleccionadas = []
        chakra_gastado = 0

        for habilidad in self.habilidades_var:
            if self.habilidades_var[habilidad].get():
                habilidades_seleccionadas.append(habilidad)
                chakra_gastado += self.habilidades_costo[habilidad]

        if chakra_gastado > self.personaje["Chakra"]:
            messagebox.showerror("Error", "No tienes suficiente chakra para realizar esas habilidades.")
        else:
            resultado = simular_pelea(self.personaje, habilidades_seleccionadas)
            mostrar_resultado(resultado)
            guardar_resultado(resultado)

def mostrar_resultado(resultado):
    mensaje = f"El ganador de la pelea es {resultado['Ganador']}\n"
    mensaje += f"{resultado['Perdedor']['Nombre']} quedó con {resultado['Perdedor']['Vida']} puntos de vida"

    messagebox.showinfo("Resultado", mensaje)

def guardar_resultado(resultado):
    with open("resultado.txt", "w") as file:
        file.write(f"Ganador: {resultado['Ganador']}\n")
        file.write(f"Perdedor: {resultado['Perdedor']['Nombre']}\n")
        file.write(f"Puntos de vida de {resultado['Perdedor']['Nombre']}: {resultado['Perdedor']['Vida']}\n")

def calcular_probabilidades(personaje):
    # Crear diccionario de probabilidades vacío
    probabilidades = {}
    
    # Calcular probabilidades para cada habilidad
    for habilidad, costo in personaje['habilidades'].items():
        # Probabilidad base de la habilidad es igual al costo de chakra
        probabilidad_base = costo
        
        # Modificadores basados en las estadísticas del personaje
        mod_ninjutsu = (personaje['ninjutsu'] / 10) * 5
        mod_taijutsu = (personaje['taijutsu'] / 10) * 5
        mod_genjutsu = (personaje['genjutsu'] / 10) * 5
        mod_inteligencia = (personaje['inteligencia'] / 10) * 2.5
        mod_fuerza = (personaje['fuerza'] / 10) * 2.5
        mod_defensa = (personaje['defensa'] / 10) * 2.5
        mod_velocidad = (personaje['velocidad'] / 10) * 2.5
        mod_resistencia = (personaje['resistencia'] / 10) * 2.5
        
        # Calcular probabilidad final con modificadores
        probabilidad_final = probabilidad_base + mod_ninjutsu + mod_taijutsu + mod_genjutsu + mod_inteligencia + mod_fuerza + mod_defensa + mod_velocidad + mod_resistencia
        
        # Añadir probabilidad al diccionario de probabilidades
        probabilidades[habilidad] = probabilidad_final
        
    return probabilidades

def calcular_golpe(personaje):
    # Calcular la probabilidad de golpe fuerte y normal
    prob_golpe_fuerte = calcular_probabilidades(personaje)['golpe fuerte']
    prob_golpe_normal = calcular_probabilidades(personaje)['golpe normal']
    
    # Generar número aleatorio entre 1 y 100
    num_aleatorio = random.randint(1, 100)
    
    # Determinar si el golpe es fuerte o normal
    if num_aleatorio <= prob_golpe_fuerte:
        return 'golpe fuerte'
    elif num_aleatorio <= prob_golpe_normal:
        return 'golpe normal'
    else:
        return 'falla'

def simular_pelea(jugador1, jugador2):
    # Inicializar variables
    chakra_jugador1 = jugador1['Chakra']
    chakra_jugador2 = jugador2['Chakra']
    resultado = {'Ganador': None, 'Perdedor': None, 'Razon': None}

    # Mientras ambos jugadores tengan chakra, la pelea continua
    while chakra_jugador1 > 0 and chakra_jugador2 > 0:
        # Selección aleatoria de la habilidad de cada jugador
        habilidad_jugador1 = random.choice(jugador1['Habilidades'])
        habilidad_jugador2 = random.choice(jugador2['Habilidades'])

        # Cálculo de la probabilidad de éxito de cada habilidad
        probabilidad_jugador1 = calcular_probabilidad(habilidad_jugador1, jugador1)
        probabilidad_jugador2 = calcular_probabilidad(habilidad_jugador2, jugador2)

        # El jugador con mayor probabilidad de éxito realiza su habilidad
        if probabilidad_jugador1 >= probabilidad_jugador2:
            chakra_jugador2 -= habilidad_jugador1['Costo de chakra']
            print(f"{jugador1['Nombre']} usa {habilidad_jugador1['Nombre']} y le hace {habilidad_jugador1['Danio']} puntos de daño a {jugador2['Nombre']}")
        else:
            chakra_jugador1 -= habilidad_jugador2['Costo de chakra']
            print(f"{jugador2['Nombre']} usa {habilidad_jugador2['Nombre']} y le hace {habilidad_jugador2['Danio']} puntos de daño a {jugador1['Nombre']}")

    # Determinar el ganador y perdedor de la pelea
    if chakra_jugador1 > 0:
        resultado['Ganador'] = jugador1['Nombre']
        resultado['Perdedor'] = jugador2['Nombre']
        resultado['Razon'] = f"{jugador2['Nombre']} se quedó sin chakra"
    else:
        resultado['Ganador'] = jugador2['Nombre']
        resultado['Perdedor'] = jugador1['Nombre']
        resultado['Razon'] = f"{jugador1['Nombre']} se quedó sin chakra"

    return resultado

def guardar_resultados(nombre_archivo, resultado):
    try:
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(f"Resultado de la pelea: {resultado}")
            print(f"Los resultados de la pelea se han guardado en {nombre_archivo}")
    except IOError:
        print("Error al guardar los resultados de la pelea.")

nombre_archivo = input("Ingrese el nombre del archivo para guardar los resultados: ")
if not nombre_archivo.endswith('.txt'):
    nombre_archivo += '.txt'

guardar_resultados(nombre_archivo, resultado)

