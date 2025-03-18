# RootFinderPy

Una aplicación de escritorio moderna con interfaz gráfica para encontrar raíces de funciones mediante métodos numéricos iterativos, desarrollada en Python con Tkinter.

![RootFinderPy Screenshot](https://github.com/Carlos1AB1/metodo-biseccion-y-falsa-posicion/raw/main/app.png)


## Características

- Implementación de métodos numéricos para cálculo de raíces:
  - Método de Bisección
  - Método de Falsa Posición (Regula Falsi)
- Interfaz gráfica moderna e intuitiva
- Visualización en tiempo real de la función y la aproximación de la raíz
- Tabla detallada de resultados con seguimiento de iteraciones
- Visualización del error relativo aproximado en cada iteración
- Validación de intervalos para garantizar la existencia de una raíz

## Requisitos

- Python 3.6+
- Bibliotecas:
  - numpy
  - matplotlib
  - pandas
  - tkinter (incluido en la mayoría de las instalaciones de Python)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/username/RootFinderPy.git
   cd RootFinderPy
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requisitos.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso

1. Ingresa la función matemática en la casilla "Función f(x)" utilizando sintaxis de Python.
   - Ejemplo: `x**3 - 4*x + 1`
   - Puedes usar funciones de numpy como `np.sin(x)`, `np.exp(x)`, etc.

2. Define el intervalo [a, b] donde buscar la raíz.
   - Nota: La función debe cambiar de signo en este intervalo.

3. Ajusta la tolerancia y el número máximo de iteraciones según sea necesario.

4. Selecciona el método numérico a utilizar: Bisección o Falsa Posición.

5. Haz clic en "Calcular" para encontrar la raíz y visualizar los resultados.

## Estructura del Proyecto

```
RootFinderPy/
├── main.py                 # Punto de entrada principal
├── interfaz.py             # Interfaz gráfica de usuario
├── metodos.py              # Implementación de métodos numéricos
├── logo.ico                # Icono de la aplicación
├── requisitos.txt          # Dependencias del proyecto
└── README.md               # Este archivo
```

## Métodos Implementados

### Método de Bisección

Técnica de búsqueda de raíces que divide repetidamente un intervalo y selecciona el subintervalo donde debe estar la raíz. Garantiza la convergencia para funciones continuas con un cambio de signo en el intervalo.

### Método de Falsa Posición (Regula Falsi)

Método numérico que combina características de los métodos de bisección y secante. Utiliza la interpolación lineal para estimar la raíz, mejorando la velocidad de convergencia respecto al método de bisección.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios
4. Haz commit de tus cambios (`git commit -m 'Add amazing feature'`)
5. Haz push a la rama (`git push origin feature/amazing-feature`)
6. Abre un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Agradecimientos

- Desarrollado por Carlos Arturo Baron Estrada y Sebastian Ordoñez Giraldo
- Inspirado en los métodos numéricos para el cálculo de raíces en análisis numérico
