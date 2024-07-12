import pandas as pd
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import ttk

# Estilo para la interfaz
def configurar_estilo():
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Tema 'clam' para un mejor aspecto
    estilo.configure('TLabel', background='#E8E8E8', font=('Helvetica', 10))
    estilo.configure('TButton', font=('Helvetica', 10))
    estilo.configure('TCombobox', font=('Helvetica', 10))
    estilo.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')])
    estilo.map('TCombobox', selectbackground=[('readonly', '#E8E8E8')])
    estilo.map('TCombobox', selectforeground=[('readonly', 'black')])

# Base de Datos del terreno
data = {
    'terreno': ['Parcela 1', 'Parcela 2', 'Parcela 3', 'Parcela 4', 'Parcela 5', 'Parcela 6', 'Parcela 7', 'Parcela 8', 'Parcela 9', 'Parcela 10'],
    'cultivo': ['Tomate', 'Pepino', 'Arroz', 'Papa', 'Maíz', 'Zanahoria', 'Lechuga', 'Cebolla', 'Frijol', 'Trigo'],
    'insumos': [104, 122, 64, 123, 57, 185, 174, 23, 195, 25],  # Insumos necesarios
    'produccion': [216, 158, 355, 187, 251, 164, 142, 199, 214, 238],  # Producción esperada
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

# Función para encontrar la parcela más recomendada
def encontrar_mejor_parcela(cultivo):
    cluster = df[df['cultivo'] == cultivo]['cluster'].values[0]
    terrenos_cluster = df[df['cluster'] == cluster]
    mejor_parcela = terrenos_cluster.loc[terrenos_cluster['infertilidad'] == 0].sort_values(by=['produccion'], ascending=False).head(1)
    return mejor_parcela['terreno'].values[0] if not mejor_parcela.empty else 'No hay recomendaciones disponibles'

# Función para encontrar el grupo de mejor productividad
def encontrar_mejor_grupo():
    grupo_mejor_productividad = df.groupby('cluster')['produccion'].mean().idxmax()
    return grupo_mejor_productividad

# Función para buscar la mejor parcela en el grupo de mejor productividad
def mejor_parcela_en_mejor_grupo():
    mejor_grupo = encontrar_mejor_grupo()
    terrenos_mejor_grupo = df[df['cluster'] == mejor_grupo]
    mejor_parcela = terrenos_mejor_grupo.loc[terrenos_mejor_grupo['infertilidad'] == 0].sort_values(by=['produccion'], ascending=False).head(1)
    return mejor_parcela['terreno'].values[0] if not mejor_parcela.empty else 'No hay recomendaciones disponibles'

# Función para mostrar la mejor parcela para cada producto
def mejor_parcela_para_cada_producto():
    resultados = {}
    for cultivo in df['cultivo'].unique():
        mejor_parcela = encontrar_mejor_parcela(cultivo)
        resultados[cultivo] = mejor_parcela
    return resultados

# Crear la interfaz gráfica
def crear_interfaz():
    root = tk.Tk()
    root.title("Análisis del Terreno Agrícola Santiago De Cuba")
    configurar_estilo()  # Aplicar el estilo configurado

    # Etiqueta y menú desplegable para seleccionar el cultivo
    ttk.Label(root, text="Selecciona un Cultivo:").grid(column=0, row=0, padx=10, pady=10)
    cultivo_seleccionado = tk.StringVar()
    cultivo_menu = ttk.Combobox(root, textvariable=cultivo_seleccionado, state='readonly')
    cultivo_menu['values'] = df['cultivo'].tolist()
    cultivo_menu.grid(column=1, row=0, padx=10, pady=10)

    # Función para mostrar los resultados y la mejor parcela
    def mostrar_resultados():
        cultivo = cultivo_seleccionado.get()
        if cultivo:
            recomendaciones = obtener_recomendaciones(cultivo)
            mejor_parcela = encontrar_mejor_parcela(cultivo)
            mejor_grupo = encontrar_mejor_grupo()
            mejor_parcela_grupo = mejor_parcela_en_mejor_grupo()
            mejores_parcelas_productos = mejor_parcela_para_cada_producto()
            resultado_texto.set(f"Recomendaciones:\n{recomendaciones.to_string(index=False)}\n\nMejor Parcela: {mejor_parcela}\n\nMejor Grupo: {mejor_grupo}\n\nMejor Parcela en Mejor Grupo: {mejor_parcela_grupo}\n\nMejor Parcela para Cada Producto: {mejores_parcelas_productos}")

    # Botón para obtener los resultados
    ttk.Button(root, text="Obtener Resultados", command=mostrar_resultados).grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    # Etiqueta para mostrar los resultados y la mejor parcela
    resultado_texto = tk.StringVar()
    ttk.Label(root, textvariable=resultado_texto, background='white', relief='sunken', width=100, anchor='w').grid(column=0, row=2, columnspan=2, padx=100, pady=100)

    root.mainloop()

# Ejecutar la interfaz gráfica
crear_interfaz()
