import pandas as pd
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import ttk

# Base de Datos del terreno
data = {
    'terreno': ['Parcela 1', 'Parcela 2', 'Parcela 3', 'Parcela 4', 'Parcela 5', 'Parcela 6', 'Parcela 7', 'Parcela 8', 'Parcela 9', 'Parcela 10'],
    'cultivo': ['Tomate', 'Pepino', 'Arroz', 'Papa', 'Maíz', 'Zanahoria', 'Lechuga', 'Cebolla', 'Frijol', 'Trigo'],
    'insumos': [100, 120, 60, 120, 50, 180, 170, 20, 195, 25],  # Insumos necesarios
    'produccion': [200, 150, 300, 180, 250, 160, 140, 190, 210, 230],  # Producción esperada
    'infertilidad': [0, 0, 1, 0, 1, 0, 0, 1, 0, 1]  # 0: fértil, 1: infértil
}

# Creación del DataFrame
df = pd.DataFrame(data)

# Seleccionar características para clustering
X = df[['insumos', 'produccion']]

# Aplicar K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Función para obtener recomendaciones basadas en clustering
def obtener_recomendaciones(cultivo):
    cluster = df[df['cultivo'] == cultivo]['cluster'].values[0]
    terrenos_cluster = df[df['cluster'] == cluster]
    return terrenos_cluster[['terreno', 'insumos', 'produccion', 'infertilidad']]

# Crear la interfaz gráfica
def crear_interfaz():
    root = tk.Tk()
    root.title("Análisis del Terreno Agrícola Santiago De Cuba")

    # Etiqueta y menú desplegable para seleccionar el cultivo
    ttk.Label(root, text="Selecciona un Cultivo:").grid(column=0, row=0, padx=10, pady=10)
    cultivo_seleccionado = tk.StringVar()
    cultivo_menu = ttk.Combobox(root, textvariable=cultivo_seleccionado)
    cultivo_menu['values'] = df['cultivo'].tolist()
    cultivo_menu.grid(column=1, row=0, padx=10, pady=10)

    # Función para mostrar los resultados
    def mostrar_resultados():
        cultivo = cultivo_seleccionado.get()
        if cultivo:
            recomendaciones = obtener_recomendaciones(cultivo)
            resultado_texto.set(recomendaciones.to_string(index=False))

    # Botón para obtener los resultados
    ttk.Button(root, text="Obtener Resultados", command=mostrar_resultados).grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    # Etiqueta para mostrar los resultados
    resultado_texto = tk.StringVar()
    ttk.Label(root, textvariable=resultado_texto).grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    root.mainloop()

# Ejecutar la interfaz gráfica
crear_interfaz()
