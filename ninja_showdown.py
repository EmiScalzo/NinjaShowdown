import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

habilidades_df = pd.read_excel("habilidades.xlsx")
personajes_df = pd.read_excel("personajes.xlsx")

# Crear ventana
ventana = tk.Tk()
ventana.title("Ninja Showdown")

# Obtener nombres de los personajes
nombres_personajes = list(personajes_df["nombre"])

# Crear variables Tkinter para las habilidades seleccionadas de cada personaje
seleccion_habilidades = {}
for nombre in nombres_personajes:
    seleccion_habilidades[nombre] = {}
    for _, habilidad in habilidades_df.iterrows():
        seleccion_habilidades[nombre][habilidad["nombre"]] = tk.BooleanVar()

# Función para obtener las habilidades seleccionadas de un personaje
def obtener_habilidades(nombre):
    habilidades_seleccionadas = []
    for habilidad, seleccionada in seleccion_habilidades[nombre].items():
        if seleccionada.get():
            habilidades_seleccionadas.append(habilidad)
    return habilidades_seleccionadas

# Función para validar que cada personaje tenga al menos una habilidad seleccionada
def validar_seleccion_habilidades():
    for nombre in nombres_personajes:
        habilidades_seleccionadas = obtener_habilidades(nombre)
        if len(habilidades_seleccionadas) == 0:
            messagebox.showerror("Error", f"El personaje '{nombre}' debe tener al menos una habilidad seleccionada.")
            return False
    return True

# Función para cerrar la ventana de selección de habilidades
def cerrar_seleccion_habilidades():
    if validar_seleccion_habilidades():
        ventana.quit()

# Crear caja de selección de habilidades para cada personaje
for i, nombre in enumerate(nombres_personajes):
    ttk.Label(ventana, text=f"Habilidades de {nombre}:").grid(column=0, row=i)
    for j, (_, habilidad) in enumerate(habilidades_df.iterrows()):
        ttk.Checkbutton(ventana, text=habilidad["nombre"], variable=seleccion_habilidades[nombre][habilidad["nombre"]]).grid(column=j+1, row=i)

# Crear botón para confirmar selección de habilidades
boton_confirmar = ttk.Button(ventana, text="Confirmar", command=cerrar_seleccion_habilidades)
boton_confirmar.grid(column=len(habilidades_df)+1, row=len(nombres_personajes))

# Iniciar ventana
ventana.mainloop()

# Cálculo de la probabilidad de éxito de las habilidades
def calculate_success_probability(attacker, defender, chosen_ability):
    attacker_attribute = attacker[chosen_ability['attribute']]
    defender_attribute = defender[chosen_ability['counter_attribute']]

    # Probabilidad base de éxito de la habilidad
    success_probability = chosen_ability['base_success_probability']

    # Se modifican los atributos según las estadísticas de cada personaje
    attacker_attribute *= (1 + attacker['stats'][chosen_ability['attribute']]/100)
    defender_attribute *= (1 + defender['stats'][chosen_ability['counter_attribute']]/100)

    # Se modifica la probabilidad base de éxito según la diferencia de atributos
    attribute_difference = attacker_attribute - defender_attribute
    success_probability += attribute_difference * chosen_ability['attribute_multiplier']

    # Limita la probabilidad de éxito a un rango de 0 a 1
    success_probability = max(min(success_probability, 1), 0)

    return success_probability

def simular_pelea(jugador1, jugador2, habilidades):
    print("¡La pelea ha comenzado!")
    turno = 1
    jugador_activo = jugador1
    jugador_inactivo = jugador2
    while True:
        print("Turno", turno, ": Es el turno de", jugador_activo.nombre)
        habilidad = seleccionar_habilidad(jugador_activo, habilidades)
        if habilidad is None:
            print("La pelea ha sido cancelada.")
            return
        print(jugador_activo.nombre, "ha utilizado", habilidad.nombre)
        exito = calcular_exito(habilidad, jugador_activo, jugador_inactivo)
        if exito:
            dano = calcular_dano(habilidad, jugador_activo, jugador_inactivo)
            print(jugador_inactivo.nombre, "ha recibido", dano, "de daño.")
            jugador_inactivo.vida -= dano
            if jugador_inactivo.vida <= 0:
                print("¡", jugador_activo.nombre, "ha ganado la pelea!")
                registrar_resultado(jugador_activo, jugador_inactivo, True)
                return
        else:
            print(habilidad.nombre, "ha fallado.")
        turno += 1
        jugador_activo, jugador_inactivo = jugador_inactivo, jugador_activo
        if turno > MAX_TURNOS:
            print("¡La pelea ha terminado en empate!")
            registrar_resultado(jugador1, jugador2, False)
            return

def guardar_resultados(resultado, archivo_salida):
    with open(archivo_salida, "w") as file:
        file.write("Resultado de la pelea:\n")
        file.write(resultado)

