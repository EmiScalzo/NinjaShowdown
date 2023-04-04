import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import random

# Cargar datos de personajes y habilidades
personajes = pd.read_excel('personajes.xlsx')
habilidades = pd.read_excel('habilidades.xlsx')

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Juego de simulación de pelea de Naruto")

# Crear frame para seleccionar personajes
frame_personajes = ttk.Frame(ventana, padding=10)
frame_personajes.pack()

# Crear etiqueta para seleccionar personaje 1
etiqueta_personaje1 = ttk.Label(frame_personajes, text="Selecciona el Personaje 1:")
etiqueta_personaje1.grid(column=0, row=0)

# Crear lista desplegable para seleccionar personaje 1
opciones_personaje1 = list(personajes['Nombre'])
seleccion_personaje1 = tk.StringVar()
opcion_personaje1 = ttk.Combobox(frame_personajes, width=20, textvariable=seleccion_personaje1, values=opciones_personaje1)
opcion_personaje1.grid(column=1, row=0)

# Crear etiqueta para seleccionar personaje 2
etiqueta_personaje2 = ttk.Label(frame_personajes, text="Selecciona el Personaje 2:")
etiqueta_personaje2.grid(column=0, row=1)

# Crear lista desplegable para seleccionar personaje 2
opciones_personaje2 = list(personajes['Nombre'])
seleccion_personaje2 = tk.StringVar()
opcion_personaje2 = ttk.Combobox(frame_personajes, width=20, textvariable=seleccion_personaje2, values=opciones_personaje2)
opcion_personaje2.grid(column=1, row=1)

# Crear botón para avanzar a la selección de habilidades
boton_personajes = ttk.Button(frame_personajes, text="Siguiente", command=lambda: seleccionar_habilidades())
boton_personajes.grid(column=1, row=2)

# Función para ocultar el frame de selección de personajes y mostrar el frame de selección de habilidades
def seleccionar_habilidades():
    frame_personajes.pack_forget()
    frame_habilidades.pack()
    etiqueta_personaje_habilidades.config(text="Selecciona las habilidades para " + seleccion_personaje1.get() + " y " + seleccion_personaje2.get())

def seleccionar_habilidades(personajes, habilidades):
    """
    Esta función permite al usuario seleccionar las habilidades que cada personaje utilizará durante la pelea.
    Se calcula la probabilidad de que cada habilidad tenga éxito basándose en los atributos y estadísticas del personaje que la utiliza.
    Retorna una lista de diccionarios con las habilidades seleccionadas y su probabilidad de éxito.
    """
    habilidades_seleccionadas = []

    for personaje in personajes:
        # Seleccionar habilidades para el personaje actual
        print(f"\nSelecciona las habilidades para {personaje['Nombre']}:")
        habilidades_personaje = []
        for i, habilidad in enumerate(habilidades):
            print(f"{i+1}. {habilidad['Nombre']} - Chakra: {habilidad['Chakra']} - Daño: {habilidad['Daño']} - Probabilidad de éxito: {habilidad['Probabilidad']}")
            while True:
                seleccion = input("Selecciona (S/N): ")
                if seleccion.upper() == 'S':
                    habilidades_personaje.append(habilidad)
                    break
                elif seleccion.upper() == 'N':
                    break
                else:
                    print("Opción no válida, intenta de nuevo.")

        # Calcular probabilidad de éxito de las habilidades seleccionadas
        print(f"\nCalculando la probabilidad de éxito para las habilidades de {personaje['Nombre']}...")
        for habilidad in habilidades_personaje:
            habilidad['Probabilidad'] = round(habilidad['Probabilidad'] + (personaje['Habilidad'] / 100), 2)

        habilidades_seleccionadas.append({
            'Personaje': personaje['Nombre'],
            'Habilidades': habilidades_personaje
        })

    return habilidades_seleccionadas

def calcular_probabilidades(personaje, habilidades):
    """
    Calcula la probabilidad de éxito de cada habilidad del personaje
    basándose en sus atributos y estadísticas.

    Args:
    - personaje: diccionario con los datos del personaje
    - habilidades: lista de diccionarios con los datos de las habilidades

    Returns:
    - dict: diccionario con las probabilidades de éxito de cada habilidad
    """
    probabilidades = {}
    for habilidad in habilidades:
        # Calcular la probabilidad de éxito de la habilidad
        prob = (habilidad["nivel"] * 0.2 + personaje["chakra"] * 0.1 + personaje["destreza"] * 0.1
                + personaje["inteligencia"] * 0.1 + personaje["fuerza"] * 0.1)
        probabilidades[habilidad["nombre"]] = round(prob, 2)
    return probabilidades

# Parte 5: Simulación de la pelea

# Crear una lista con los personajes que participarán en la pelea
peleadores = []
for i in range(cantidad_peleadores):
    peleadores.append(personajes_elegidos[i])

# Crear una lista con las habilidades seleccionadas para cada personaje
habilidades_peleadores = []
for i in range(cantidad_peleadores):
    habilidades = []
    for j in range(cantidad_habilidades):
        if habilidades_seleccionadas[i][j] == 1:
            habilidades.append(habilidades_disponibles[j])
    habilidades_peleadores.append(habilidades)

# Crear una matriz de probabilidades de éxito de las habilidades
probabilidades_exito = []
for i in range(cantidad_peleadores):
    habilidades = habilidades_peleadores[i]
    probabilidades_personaje = []
    for j in range(len(habilidades)):
        habilidad = habilidades[j]
        probabilidad_exito = calcular_probabilidad_exito(personajes_elegidos[i], habilidad)
        probabilidades_personaje.append(probabilidad_exito)
    probabilidades_exito.append(probabilidades_personaje)

# Crear una lista con los resultados de la pelea
resultados_pelea = []
for i in range(cantidad_peleadores):
    resultados_personaje = []
    for j in range(cantidad_habilidades):
        if habilidades_seleccionadas[i][j] == 1:
            resultados_habilidad = []
            for k in range(cantidad_peleadores):
                if k != i:
                    resultado_habilidad = simular_pelea(personajes_elegidos[i], habilidades_disponibles[j], 
                                                         probabilidades_exito[i][j], peleadores[k])
                    resultados_habilidad.append(resultado_habilidad)
            resultados_personaje.append(resultados_habilidad)
    resultados_pelea.append(resultados_personaje)

# Guardar los resultados en un archivo de texto
with open("resultados_pelea.txt", "w") as archivo_resultados:
    for i in range(cantidad_peleadores):
        archivo_resultados.write("Resultados para " + peleadores[i]["Nombre"] + "\n\n")
        for j in range(cantidad_habilidades):
            if habilidades_seleccionadas[i][j] == 1:
                archivo_resultados.write("Habilidad: " + habilidades_disponibles[j]["Nombre"] + "\n")
                for k in range(cantidad_peleadores):
                    if k != i:
                        archivo_resultados.write("Contra " + peleadores[k]["Nombre"] + ": ")
                        archivo_resultados.write(str(resultados_pelea[i][j][k]) + "\n")
                archivo_resultados.write("\n")

def guardar_resultados(resultados):
    # Pedir al usuario el nombre del archivo de salida
    nombre_archivo = input("Ingrese el nombre del archivo de salida: ")

    # Verificar si la extensión es .txt o .xlsx
    if nombre_archivo.endswith('.txt'):
        with open(nombre_archivo, 'w') as f:
            # Escribir los resultados en el archivo de texto
            for r in resultados:
                f.write(r + '\n')
        print(f"Resultados guardados en el archivo {nombre_archivo}")
    elif nombre_archivo.endswith('.xlsx'):
        # Crear un nuevo archivo de excel
        workbook = xlsxwriter.Workbook(nombre_archivo)

        # Crear una nueva hoja
        worksheet = workbook.add_worksheet()

        # Escribir los resultados en la hoja de excel
        row = 0
        col = 0
        for r in resultados:
            worksheet.write(row, col, r)
            row += 1

        # Cerrar el archivo de excel
        workbook.close()
        print(f"Resultados guardados en el archivo {nombre_archivo}")
    else:
        print("Extensión de archivo no válida. Use .txt o .xlsx")
