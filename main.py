import tkinter as tk
from tkinter import ttk, messagebox
import random
from openpyxl import Workbook


# Función uniforme global
def uniforme(a: int, b: int, rnd: float) -> float:
    return round(a + rnd * (b - a), 4)


# Función uniforme global


class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Venta de Pastelitos")

        # ----- FRAME DE PARÁMETROS GENERALES -----
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

        self.simular_btn = tk.Button(self.param_frame, text="Simular", command=self.simular)
        self.simular_btn.grid(row=0, column=6, padx=10)
        tk.Button(self.param_frame, text="Exportar a Excel", command=self.exportar_excel).grid(row=0, column=7, padx=10)

        # ----- FRAME PARA PARÁMETROS VARIABLES -----
        self.variables_frame = tk.LabelFrame(root, text="Parámetros de Demanda y Precios")
        self.variables_frame.pack(pady=10)

        self.demandas = [1, 2, 5, 6, 7, 8, 10]
        tk.Label(self.variables_frame, text="Demanda:").grid(row=0, column=1, columnspan=7)
        for idx, d in enumerate(self.demandas):
            tk.Label(self.variables_frame, text=str(d)).grid(row=1, column=idx + 1)

        tk.Label(self.variables_frame, text="Probabilidades:").grid(row=2, column=0)
        self.prob_entries = []
        for idx in range(len(self.demandas)):
            e = tk.Entry(self.variables_frame, width=5)
            e.insert(0, [0.1, 0.2, 0.4, 0.1, 0.1, 0.05, 0.05][idx])
            e.grid(row=2, column=idx + 1)
            self.prob_entries.append(e)

        tk.Label(self.variables_frame, text="Precio por unidad:").grid(row=3, column=0)
        self.precio_entries = []
        for idx in range(len(self.demandas)):
            e = tk.Entry(self.variables_frame, width=5)
            e.insert(0, [100, 100, 100, 80, 80, 80, 80][idx])
            e.grid(row=3, column=idx + 1)
            self.precio_entries.append(e)

        # ----- TREEVIEW PARA RESULTADOS -----
        self.tree = ttk.Treeview(root, columns=(
            'Día', 'Clientes', 'Demanda Total', 'Vendidos', 'Sobrantes', 'Acum. Sobrantes', 'Prom. Sobrantes',
            'Producción', 'Costo Total', 'Ingresos', 'Ganancia', 'Acum. Ganancia', 'Prom. Ganancia'), show='headings')

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=115)

        self.tree.pack(expand=True, fill='both')
        scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.datos_simulados = []

    def uniforme(a: int, b: int, rnd: float) -> float:
        return round(a + rnd * (b - a), 4)

    def simular_dia(self, dia, fila_anterior, produccion, demanda_posible, probabilidades, precio_por_demanda):
        #print(f"🧾 Día {dia} - Producción: {produccion} pastelitos")
        demandas_clientes = []
        rnds_demandas = []
        rnd_clientes = random.random()
        clientes = int(uniforme(10, 30, rnd_clientes))
        #print(f"Random generado para clientes: {rnd_clientes} → Clientes: {clientes}")
        demanda_total = 0
        ingresos = 0

        for _ in range(clientes):

            rnd_demanda = random.random()
            rnds_demandas.append(rnd_demanda)
            demanda = random.choices(demanda_posible, probabilidades)[0]
            demandas_clientes.append(demanda)
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

        #print(f"Clientes: {clientes}")
        #print(f"Demandas generadas: {demandas_clientes}")
        #precios_asociados = [precio_por_demanda[d] for d in demandas_clientes]
        #print(f"Precios asociados: {precios_asociados}")
        #print(f"Randoms usados para demanda: {rnds_demandas}")

        acum_sobrantes = fila_anterior[
                             'Acum. Sobrantes'] + sobrantes if 'Acum. Sobrantes' in fila_anterior else sobrantes
        acum_ganancia = fila_anterior['Acum. Ganancia'] + ganancia if 'Acum. Ganancia' in fila_anterior else ganancia

        prom_sobrantes = acum_sobrantes / dia
        prom_ganancia = acum_ganancia / dia

        return {
            'Día': dia,
            'Clientes': clientes,
            'Demanda Total': demanda_total,
            'Vendidos': vendidos,
            'Sobrantes': sobrantes,
            'Acum. Sobrantes': acum_sobrantes,
            'Prom. Sobrantes': round(prom_sobrantes, 2),
            'Producción': produccion,
            'Costo Total': costo_total,
            'Ingresos': ingresos,
            'Ganancia': ganancia,
            'Acum. Ganancia': acum_ganancia,
            'Prom. Ganancia': round(prom_ganancia, 2),
        }

    def simular(self):
        self.simular_btn.config(state='disabled')
        self.result_label.config(text='⏳ Simulando...')
        #print("📦 Precios por unidad según demanda ingresados:")
        self.tree.delete(*self.tree.get_children())
        try:
            n = int(self.entry_n.get())
            i = int(self.entry_i.get())
            j = int(self.entry_j.get())
            probabilidades = [float(e.get()) for e in self.prob_entries]
            precios = [int(e.get()) for e in self.precio_entries]
        except ValueError:
            self.result_label.config(text="⚠️ Ingresá valores numéricos válidos.")
            self.progress["value"] = 0
            self.simular_btn.config(state='normal')
            return

        if not (1 <= i <= j <= n):
            self.result_label.config(text="⚠️ El rango debe cumplir: 1 ≤ i ≤ j ≤ N.")
            self.simular_btn.config(state='normal')
            return

        if abs(sum(probabilidades) - 1.0) > 0.01:
            self.result_label.config(text="⚠️ La suma de probabilidades debe ser 1.0")
            self.simular_btn.config(state='normal')
            return

        demanda_posible = self.demandas
        precio_por_demanda = dict(zip(demanda_posible, precios))
        for d in demanda_posible:
            print(f"Demanda {d}: ${precio_por_demanda[d]}")

        self.datos_simulados = []
        fila_anterior = {'Sobrantes': 0, 'Acum. Sobrantes': 0, 'Acum. Ganancia': 0}

        self.progress["maximum"] = n
        for dia in range(1, n + 1):
            produccion = 200
            fila_actual = self.simular_dia(dia, fila_anterior, produccion, demanda_posible, probabilidades,
                                           precio_por_demanda)
            self.progress["value"] = dia
            self.root.update_idletasks()
            self.datos_simulados.append(fila_actual)
            fila_anterior = fila_actual

        for fila in self.datos_simulados[i - 1:j]:
            valores = [fila[col] for col in self.tree['columns']]
            self.tree.insert('', 'end', values=valores)

        ultima = self.datos_simulados[-1]
        promedio_sobrantes = ultima['Prom. Sobrantes']
        promedio_ganancia = ultima['Prom. Ganancia']

        texto_resultado = f"📊 Última fila (Día {ultima['Día']}): Ganancia ${ultima['Ganancia']}, Sobrantes: {ultima['Sobrantes']}\n"
        texto_resultado += f"Promedio de sobrantes por día: {promedio_sobrantes:.2f} pastelitos\n"
        texto_resultado += f"Promedio de ganancia por día: ${promedio_ganancia:.2f}"
        self.progress["value"] = 0
        self.result_label.config(text=texto_resultado)
        self.simular_btn.config(state='normal')

    def exportar_excel(self):
        if not self.datos_simulados:
            messagebox.showwarning("Exportar", "Primero ejecutá una simulación.")
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Simulación Pastelitos"

        encabezados = list(self.datos_simulados[0].keys())
        ws.append(encabezados)

        for fila in self.datos_simulados:
            ws.append([fila[col] for col in encabezados])

        try:
            wb.save("simulacion_pastelitos.xlsx")
            messagebox.showinfo("Éxito", "Archivo Excel guardado como 'simulacion_pastelitos.xlsx'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
