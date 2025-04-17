import tkinter as tk
from tkinter import ttk
import random

demanda_posible = [1, 2, 5, 6, 7, 8, 10]
probabilidades = [0.1, 0.2, 0.4, 0.1, 0.1, 0.05, 0.05]
precio_por_demanda = {1: 100, 2: 100, 5: 100, 6: 80, 7: 80, 8: 80, 10: 80}

def simular_dia(dia, fila_anterior, produccion):
    clientes = random.randint(10, 30)
    demanda_total = 0
    ingresos = 0

    for _ in range(clientes):
        demanda = random.choices(demanda_posible, probabilidades)[0]
        precio = precio_por_demanda[demanda]
        ingresos += min(demanda, produccion - demanda_total) * precio
        demanda_total += demanda
        if demanda_total >= produccion:
            break

    vendidos = min(demanda_total, produccion)
    sobrantes = max(0, produccion - vendidos)
    costo_unitario = 30
    costo_total = produccion * costo_unitario
    ganancia = ingresos - costo_total

    return {
        'Día': dia,
        'Clientes': clientes,
        'Demanda Total': demanda_total,
        'Vendidos': vendidos,
        'Sobrantes': sobrantes,
        'Producción': produccion,
        'Costo Total': costo_total,
        'Ingresos': ingresos,
        'Ganancia': ganancia,
    }

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Venta de Pastelitos")

        self.param_frame = tk.Frame(root)
        self.param_frame.pack(pady=10)

        tk.Label(self.param_frame, text="Días a simular (N):").grid(row=0, column=0)
        tk.Label(self.param_frame, text="Desde iteración (i):").grid(row=0, column=2)
        tk.Label(self.param_frame, text="Hasta iteración (j):").grid(row=0, column=4)

        self.entry_n = tk.Entry(self.param_frame, width=10)
        self.entry_i = tk.Entry(self.param_frame, width=10)
        self.entry_j = tk.Entry(self.param_frame, width=10)

        self.entry_n.grid(row=0, column=1, padx=5)
        self.entry_i.grid(row=0, column=3, padx=5)
        self.entry_j.grid(row=0, column=5, padx=5)

        tk.Button(self.param_frame, text="Simular", command=self.simular).grid(row=0, column=6, padx=10)

        self.tree = ttk.Treeview(root, columns=(
            'Día', 'Clientes', 'Demanda Total', 'Vendidos', 'Sobrantes', 'Producción',
            'Costo Total', 'Ingresos', 'Ganancia'), show='headings')

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=100)

        self.tree.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

    def simular(self):
        self.tree.delete(*self.tree.get_children())
        try:
            n = int(self.entry_n.get())
            i = int(self.entry_i.get())
            j = int(self.entry_j.get())
        except ValueError:
            self.result_label.config(text="⚠️ Ingresá valores numéricos válidos.")
            return

        if not (1 <= i <= j <= n):
            self.result_label.config(text="⚠️ El rango de iteraciones debe ser válido: 1 ≤ i ≤ j ≤ N.")
            return

        datos_simulados = []
        fila_anterior = {'Sobrantes': 0}

        for dia in range(1, n + 1):
            produccion = 180 if fila_anterior['Sobrantes'] > 50 else 200
            fila_actual = simular_dia(dia, fila_anterior, produccion)
            datos_simulados.append(fila_actual)
            fila_anterior = fila_actual

        for fila in datos_simulados[i - 1:j]:
            valores = [fila[col] for col in self.tree['columns']]
            self.tree.insert('', 'end', values=valores)

        ultima = datos_simulados[-1]
        promedio_sobrantes = sum(d['Sobrantes'] for d in datos_simulados) / n
        promedio_ganancia = sum(d['Ganancia'] for d in datos_simulados) / n

        texto_resultado = f"📊 Última fila (Día {ultima['Día']}): Ganancia ${ultima['Ganancia']}, Sobrantes: {ultima['Sobrantes']}\n"
        texto_resultado += f"Promedio de sobrantes por día: {promedio_sobrantes:.2f} pastelitos\n"
        texto_resultado += f"Promedio de ganancia por día: ${promedio_ganancia:.2f}"
        self.result_label.config(text=texto_resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
