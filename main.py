import tkinter as tk
from tkinter import ttk, messagebox
import random
import pandas as pd

# Configuraciones generales por defecto
COSTO_PASTELITO = 30
CANTIDAD_PRODUCCION = 200
DEMANDAS = [1, 2, 5, 6, 7, 8, 10]

# Interfaz para ingresar parámetros variables
def obtener_parametros():
    probabilidades = []
    precios = {}
    try:
        for i, d in enumerate(DEMANDAS):
            prob = float(entries_prob[d].get())
            probabilidades.append(prob)
            precios[d] = float(entries_precio[d].get())
        return probabilidades, precios
    except ValueError:
        messagebox.showerror("Error", "Probabilidades y precios deben ser números válidos.")
        return None, None

def simular_ventas(n_dias, probabilidades, precios):
    resultados = []
    for dia in range(1, n_dias + 1):
        clientes = random.randint(10, 30)
        demandas = random.choices(DEMANDAS, weights=probabilidades, k=clientes)
        total_demandado = sum(demandas)
        total_vendido = min(total_demandado, CANTIDAD_PRODUCCION)
        sobrantes = max(CANTIDAD_PRODUCCION - total_vendido, 0)
        ingresos = 0
        vendidos = 0
        for d in demandas:
            if vendidos + d <= CANTIDAD_PRODUCCION:
                ingresos += precios[d] * d
                vendidos += d
            else:
                break
        costo = CANTIDAD_PRODUCCION * COSTO_PASTELITO
        ganancia = ingresos - costo

        resultados.append({
            "Día": dia,
            "Clientes": clientes,
            "Demanda Total": total_demandado,
            "Vendidos": total_vendido,
            "Sobrantes": sobrantes,
            "Ingresos": ingresos,
            "Costo": costo,
            "Ganancia": ganancia
        })
    return pd.DataFrame(resultados)

def mostrar_resultado(df, desde, hasta):
    for row in tree.get_children():
        tree.delete(row)
    df_filtrado = df.iloc[desde:hasta]
    for _, row in df_filtrado.iterrows():
        tree.insert("", tk.END, values=list(row))

def ejecutar_simulacion():
    try:
        n = int(entry_n.get())
        i = int(entry_i.get())
        j = int(entry_j.get())
        probabilidades, precios = obtener_parametros()
        if probabilidades is None:
            return
        df = simular_ventas(n, probabilidades, precios)
        mostrar_resultado(df, i, i + j)

        promedio_sobrantes = df["Sobrantes"].mean()
        promedio_ganancia = df["Ganancia"].mean()
        ultima_fila = df.iloc[-1]

        messagebox.showinfo("Resultados", f"Promedio de sobrantes: {promedio_sobrantes:.2f}\nPromedio de ganancia: ${promedio_ganancia:.2f}\n\nÚltimo día:\n{ultima_fila.to_string()}" )
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Interfaz Gráfica
root = tk.Tk()
root.title("Simulador de Venta de Pastelitos")
root.geometry("1200x700")

frame = tk.Frame(root)
frame.pack(pady=10)

lbl_n = tk.Label(frame, text="Cantidad de días (N):")
lbl_n.grid(row=0, column=0)
entry_n = tk.Entry(frame)
entry_n.grid(row=0, column=1)

lbl_i = tk.Label(frame, text="Mostrar desde la iteración i:")
lbl_i.grid(row=1, column=0)
entry_i = tk.Entry(frame)
entry_i.grid(row=1, column=1)

lbl_j = tk.Label(frame, text="Cantidad de filas a mostrar (j):")
lbl_j.grid(row=2, column=0)
entry_j = tk.Entry(frame)
entry_j.grid(row=2, column=1)

# Entradas de probabilidades y precios
frame_param = tk.LabelFrame(root, text="Parámetros de Demanda")
frame_param.pack(padx=10, pady=10)

entries_prob = {}
entries_precio = {}

for idx, demanda in enumerate(DEMANDAS):
    tk.Label(frame_param, text=f"Demanda {demanda}").grid(row=0, column=idx+1)
    tk.Label(frame_param, text="Prob.").grid(row=1, column=0)
    e_prob = tk.Entry(frame_param, width=6)
    e_prob.insert(0, str([0.1, 0.2, 0.4, 0.1, 0.1, 0.05, 0.05][idx]))
    e_prob.grid(row=1, column=idx+1)
    entries_prob[demanda] = e_prob

    tk.Label(frame_param, text="Precio").grid(row=2, column=0)
    e_precio = tk.Entry(frame_param, width=6)
    e_precio.insert(0, str([100, 100, 100, 80, 80, 80, 80][idx]))
    e_precio.grid(row=2, column=idx+1)
    entries_precio[demanda] = e_precio

btn_simular = tk.Button(root, text="Simular", command=ejecutar_simulacion)
btn_simular.pack(pady=10)

cols = ["Día", "Clientes", "Demanda Total", "Vendidos", "Sobrantes", "Ingresos", "Costo", "Ganancia"]
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()
