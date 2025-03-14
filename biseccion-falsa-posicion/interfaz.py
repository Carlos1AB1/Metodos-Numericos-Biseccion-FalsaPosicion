import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from metodos import biseccion, falsa_posicion
import pandas as pd
from matplotlib.figure import Figure
import matplotlib as mpl


class ModernNumericApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos - Análisis de Raíces - Carlos Arturo Baron Estrada - Sebastian Ordoñez Giraldo")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f7")

        # Configuración de estilo
        self.setup_styles()
        root.iconbitmap("logo.ico")

        # Frame principal
        main_frame = ttk.Frame(root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame de entrada
        input_frame = ttk.Frame(main_frame, style="Card.TFrame")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Título
        title_label = ttk.Label(input_frame, text="Cálculo de Raíces por Métodos Iterativos",
                                style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=4, pady=(15, 20), padx=20, sticky="w")

        # Sección de parámetros
        param_frame = ttk.Frame(input_frame, style="Card.TFrame")
        param_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="ew")

        # Primera fila - Función
        ttk.Label(param_frame, text="Función f(x):", style="Param.TLabel").grid(row=0, column=0, sticky="w",
                                                                                padx=(0, 10), pady=10)
        # Crear el campo de entrada de función con placeholder
        self.func_entry = ttk.Entry(param_frame, width=40, font=("Segoe UI", 10))
        self.func_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(0, 20), pady=10)

        # Definir el placeholder
        placeholder_text = "Ejemplo: x**3 - 4*x + 1"

        # Función para borrar el placeholder cuando el usuario escribe
        def on_focus_in(event):
            if self.func_entry.get() == placeholder_text:
                self.func_entry.delete(0, tk.END)
                self.func_entry.config(foreground="black")  # Cambiar color del texto

        # Función para restaurar el placeholder si el usuario no escribe nada
        def on_focus_out(event):
            if self.func_entry.get() == "":
                self.func_entry.insert(0, placeholder_text)
                self.func_entry.config(foreground="gray")  # Cambiar color del texto

        # Insertar el placeholder y configurar los eventos
        self.func_entry.insert(0, placeholder_text)
        self.func_entry.config(foreground="gray")  # Hacer que el placeholder sea gris
        self.func_entry.bind("<FocusIn>", on_focus_in)
        self.func_entry.bind("<FocusOut>", on_focus_out)

        # Segunda fila - Límites
        ttk.Label(param_frame, text="Límite inferior (a):", style="Param.TLabel").grid(row=1, column=0, sticky="w",
                                                                                       padx=(0, 10), pady=10)
        self.a_entry = ttk.Entry(param_frame, width=12, font=("Segoe UI", 10))
        self.a_entry.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)
        self.a_entry.insert(0, "0")

        ttk.Label(param_frame, text="Límite superior (b):", style="Param.TLabel").grid(row=1, column=2, sticky="w",
                                                                                       padx=(0, 10), pady=10)
        self.b_entry = ttk.Entry(param_frame, width=12, font=("Segoe UI", 10))
        self.b_entry.grid(row=1, column=3, sticky="w", padx=(0, 20), pady=10)
        self.b_entry.insert(0, "2")

        # Tercera fila - Parámetros
        ttk.Label(param_frame, text="Tolerancia:", style="Param.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 10),
                                                                              pady=10)
        self.tol_entry = ttk.Entry(param_frame, width=12, font=("Segoe UI", 10))
        self.tol_entry.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)
        self.tol_entry.insert(0, "0.001")

        ttk.Label(param_frame, text="Máx. Iteraciones:", style="Param.TLabel").grid(row=2, column=2, sticky="w",
                                                                                    padx=(0, 10), pady=10)
        self.iter_entry = ttk.Entry(param_frame, width=12, font=("Segoe UI", 10))
        self.iter_entry.grid(row=2, column=3, sticky="w", padx=(0, 20), pady=10)
        self.iter_entry.insert(0, "50")

        # Cuarta fila - Método y botón
        ttk.Label(param_frame, text="Método:", style="Param.TLabel").grid(row=3, column=0, sticky="w", padx=(0, 10),
                                                                          pady=10)
        self.metodo_var = tk.StringVar(value="Bisección")
        self.metodo_menu = ttk.Combobox(param_frame, textvariable=self.metodo_var,
                                        values=["Bisección", "Falsa Posición"],
                                        font=("Segoe UI", 10), state="readonly", width=20)
        self.metodo_menu.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)

        self.calc_btn = ttk.Button(param_frame, text="Calcular", style="Calculate.TButton",
                                   command=self.calcular)
        self.calc_btn.grid(row=3, column=3, sticky="e", padx=(0, 20), pady=10)

        # Layout de tabla y gráfica
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Lado izquierdo - Tabla
        table_frame = ttk.Frame(content_frame, style="Card.TFrame")
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        table_title = ttk.Label(table_frame, text="Tabla de Resultados",
                                style="SubTitle.TLabel")
        table_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Tabla con scrollbar
        table_container = ttk.Frame(table_frame)
        table_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabla mejorada
        self.tree = ttk.Treeview(table_container, columns=("Iter", "a", "xr", "b", "f(xr)", "Ea"),
                                 show="headings", style="Mystyle.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de las columnas
        column_widths = {"Iter": 40, "a": 90, "xr": 90, "b": 90, "f(xr)": 100, "Ea": 90}  # Sin el '%'
        for col, width in column_widths.items():
            # Ajustar el encabezado para que "Ea%" se muestre correctamente
            header_text = "Ea (%)" if col == "Ea" else col
            self.tree.heading(col, text=header_text)
            self.tree.column(col, width=width, anchor=tk.CENTER)

        # Configurar scrollbar
        scrollbar.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)

        # Lado derecho - Gráfico
        graph_frame = ttk.Frame(content_frame, style="Card.TFrame")
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        graph_title = ttk.Label(graph_frame, text="Gráfica de la Función",
                                style="SubTitle.TLabel")
        graph_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Gráfico mejorado
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#ffffff")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#f9f9f9")
        self.fig.patch.set_facecolor("#ffffff")

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Configuración inicial de la gráfica
        self.configurar_grafica()

        # Etiqueta de estado y resultados
        self.status_frame = ttk.Frame(main_frame, style="Card.TFrame")
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.status_label = ttk.Label(self.status_frame, text="Ingrese los parámetros y presione 'Calcular'",
                                      style="Status.TLabel")
        self.status_label.pack(padx=15, pady=10)

        # Centrar la ventana
        self.center_window()

    # Remove this function from inside __init__
    # def graficar_funcion(self, func, a, b, raiz):
    #     ...

    # And add this method to the class (properly indented)
    def graficar_funcion(self, func, a, b, raiz):
        self.ax.clear()

        try:
            # Asegurar que 'a' y 'b' sean válidos para evitar problemas con sqrt(x)
            if a < 0:
                messagebox.showerror("Error",
                                     "El valor de 'a' debe ser mayor o igual a 0 para evitar errores en sqrt(x).")
                return

            # Generar puntos x de forma segura
            x_min, x_max = min(a, b) - 0.5, max(a, b) + 0.5
            x = np.linspace(x_min, x_max, 200)

            # Evaluar la función, evitando errores de cálculo
            y = []
            for xi in x:
                try:
                    yi = func(xi)
                    if np.isnan(yi) or np.isinf(yi):
                        raise ValueError
                    y.append(yi)
                except:
                    y.append(np.nan)  # Evitar crash, marcar como NaN

            # Convertir a array para facilitar manejo de NaN
            y = np.array(y)

            # Verificar si la función generó solo NaN
            if np.all(np.isnan(y)):
                messagebox.showerror("Error",
                                     "No se pueden graficar valores inválidos en la función. Revisa el intervalo.")
                return

            # Filtrar valores válidos para evitar errores en min/max
            y_valid = y[~np.isnan(y)]
            y_min, y_max = min(y_valid), max(y_valid)
            margin = (y_max - y_min) * 0.1 if (y_max - y_min) != 0 else 0.1  # Evitar división por cero

            # Graficación mejorada
            self.ax.plot(x, y, linewidth=2, color='#003F76', label="f(x)")  # Azul para la función
            self.ax.scatter([raiz], [func(raiz)], color='#B42325', s=80, zorder=3,
                            label=f"Raíz: {raiz:.6f}")  # Rojo para la raíz
            self.ax.axhline(y=0, color='black', linestyle='-', alpha=0.7)

            # Marcar el eje x
            self.ax.axhline(y=0, color='black', linestyle='-', alpha=0.7)

            # Marcar el intervalo inicial
            self.ax.axvline(x=a, color='#2ecc71', linestyle='--', alpha=0.5, label=f"a = {a}")
            self.ax.axvline(x=b, color='#9b59b6', linestyle='--', alpha=0.5, label=f"b = {b}")

            # Configurar estilo de la gráfica
            self.ax.set_facecolor('#f9f9f9')
            self.ax.set_xlabel('x', fontsize=10)
            self.ax.set_ylabel('f(x)', fontsize=10)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend(frameon=True, framealpha=0.9, fontsize=9)

            # Ajustar los límites
            self.ax.set_ylim(y_min - margin, y_max + margin)

            # Título de la gráfica
            self.ax.set_title(f"Visualización de f(x) = {self.func_entry.get()}", fontsize=10)

            # Actualizar figura
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")


    def setup_styles(self):
        # Configuración del estilo
        self.style = ttk.Style()
        self.style.configure("Main.TFrame", background="#f5f5f7")
        self.style.configure("Card.TFrame", background="#ffffff", relief=tk.RAISED)
        self.style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background="#ffffff", foreground="#333333")
        self.style.configure("SubTitle.TLabel", font=("Segoe UI", 12), background="#ffffff", foreground="#333333")
        self.style.configure("Param.TLabel", font=("Segoe UI", 10), background="#ffffff", foreground="#333333")
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), background="#ffffff", foreground="#333333")

        # Estilo para el botón
        self.style.configure("Calculate.TButton", font=("Segoe UI", 10, "bold"))

        # Estilo para la tabla
        self.style.configure("Mystyle.Treeview", font=("Segoe UI", 9))
        self.style.configure("Mystyle.Treeview.Heading", font=("Segoe UI", 9, "bold"),
                         background="#003F76", foreground="#000000")  # Azul con texto blanco

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def configurar_grafica(self):
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('f(x)', fontsize=10)
        self.ax.axhline(y=0, color='black', linestyle='-', alpha=0.7)
        self.fig.tight_layout()
        self.canvas.draw()

    def calcular(self):
        try:
            # Limpiar la tabla
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Obtener valores de entrada
            func_str = self.func_entry.get()
            func = lambda x: eval(func_str, {"np": np, "x": x})
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.iter_entry.get())
            metodo = self.metodo_var.get()

            # Verificar intervalo
            if func(a) * func(b) >= 0:
                messagebox.showerror("Error de Intervalo",
                                     "El intervalo [a,b] debe contener un cambio de signo para la función.\n"
                                     "Verifique que f(a) y f(b) tengan signos opuestos.")
                self.status_label.config(text="Error: El intervalo no tiene un cambio de signo.")
                return

            # Ejecutar el método seleccionado
            if metodo == "Bisección":
                resultado = biseccion(func, a, b, tol, max_iter)
                metodo_texto = "Bisección"
            else:
                resultado = falsa_posicion(func, a, b, tol, max_iter)
                metodo_texto = "Falsa Posición"

            # Mostrar resultados
            self.mostrar_resultados(resultado)

            # Graficar la función
            raiz = resultado[-1][2]  # Extraer la raíz final (xr)
            error = resultado[-1][5]  # Extraer el error final
            self.graficar_funcion(func, a, b, raiz)

            # Actualizar mensaje de estado
            self.status_label.config(
                text=f"Raíz encontrada: {raiz:.8f} | Error: {error if error != 'None' else 'N/A'} | "
                     f"Iteraciones: {len(resultado)} | Método: {metodo_texto}")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")

    def mostrar_resultados(self, resultado):
        # Aplicar colores alternados a las filas
        for i, fila in enumerate(resultado):
            # Formatear valores numéricos
            fila_formateada = list(fila)
            fila_formateada[0] = int(fila[0])  # Iteración como entero

            # Formatear valores numéricos cuando sea posible
            for j in range(1, 6):
                if isinstance(fila[j], (int, float)) and fila[j] != "None":
                    if abs(fila[j]) < 0.0001 or abs(fila[j]) > 10000:
                        fila_formateada[j] = f"{fila[j]:.6e}"
                    else:
                        fila_formateada[j] = f"{fila[j]:.6f}"

            # Alternar colores de las filas
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            self.tree.insert("", "end", values=fila_formateada, tags=tags)

        # Configurar colores alternos
        self.tree.tag_configure('evenrow', background='#E0E6F8')  # Azul claro institucional
        self.tree.tag_configure('oddrow', background='#FFFFFF')  # Blanco

        # Desplazarse hasta la última fila
        if len(resultado) > 0:
            self.tree.see(self.tree.get_children()[-1])


def graficar_funcion(self, func, a, b, raiz):
    self.ax.clear()

    try:
        # Asegurar que 'a' y 'b' sean válidos para evitar problemas con sqrt(x)
        if a < 0:
            messagebox.showerror("Error", "El valor de 'a' debe ser mayor o igual a 0 para evitar errores en sqrt(x).")
            return

        # Generar puntos x de forma segura
        x_min, x_max = min(a, b) - 0.5, max(a, b) + 0.5
        x = np.linspace(x_min, x_max, 200)

        # Evaluar la función, evitando errores de cálculo
        y = []
        for xi in x:
            try:
                yi = func(xi)
                if np.isnan(yi) or np.isinf(yi):
                    raise ValueError
                y.append(yi)
            except:
                y.append(np.nan)  # Evitar crash, marcar como NaN

        # Convertir a array para facilitar manejo de NaN
        y = np.array(y)

        # Verificar si la función generó solo NaN
        if np.all(np.isnan(y)):
            messagebox.showerror("Error", "No se pueden graficar valores inválidos en la función. Revisa el intervalo.")
            return

        # Filtrar valores válidos para evitar errores en min/max
        y_valid = y[~np.isnan(y)]
        y_min, y_max = min(y_valid), max(y_valid)
        margin = (y_max - y_min) * 0.1 if (y_max - y_min) != 0 else 0.1  # Evitar división por cero

        # Graficación mejorada
        self.ax.plot(x, y, linewidth=2, color='#3498db', label="f(x)")
        self.ax.scatter([raiz], [func(raiz)], color='#e74c3c', s=80, zorder=3, label=f"Raíz: {raiz:.6f}")

        # Marcar el eje x
        self.ax.axhline(y=0, color='black', linestyle='-', alpha=0.7)

        # Marcar el intervalo inicial
        self.ax.axvline(x=a, color='#2ecc71', linestyle='--', alpha=0.5, label=f"a = {a}")
        self.ax.axvline(x=b, color='#9b59b6', linestyle='--', alpha=0.5, label=f"b = {b}")

        # Configurar estilo de la gráfica
        self.ax.set_facecolor('#f9f9f9')
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('f(x)', fontsize=10)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend(frameon=True, framealpha=0.9, fontsize=9)

        # Ajustar los límites
        self.ax.set_ylim(y_min - margin, y_max + margin)

        # Título de la gráfica
        self.ax.set_title(f"Visualización de f(x) = {self.func_entry.get()}", fontsize=10)

        # Actualizar figura
        self.fig.tight_layout()
        self.canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")


def main():
    root = tk.Tk()
    app = ModernNumericApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()