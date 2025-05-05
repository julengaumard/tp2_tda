import numpy as np
import matplotlib.pyplot as plt
import random
import string
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from algoritmo import procesar_texto
from utils import performance

# Constantes globales para el análisis
SIZES_TIME_COMPLEXITY = [50, 100, 125, 150, 170, 200, 250, 300, 400]
DICTIONARY_SIZES = [ num for num in range(100, 20_001, 1000) ]
HUGE_DICTIONARY_SIZES = [ num for num in range(10_000, 1_000_000, 50_000) ]

MAX_WORD_LENGTH = 5                   # Longitud máxima de las palabras
NUMBER_OF_WORDS_IN_ONE_SENTENCE = 100   # Tamaño fijo del texto a procesar
NUMBER_OF_SENTENCES = 100                 # Cantidad de oraciones por caso

FIXED_WORD_LENGTH = 100  # Longitud constante para cada palabra del diccionario
RUNS_PER_SIZE = 1  # Número de ejecuciones por tamaño


WORKERS = 12  # Número de procesos paralelos a usar

def _process_size(size, runs_per_size, dictionary):
    """Función para medir el tiempo de ejecución para un tamaño específico."""
    print(f"Midiendo para tamaño {size}...")
    times = []
    for _ in range(runs_per_size):
        texts = [generate_valid_text(dictionary, size) for _ in range(NUMBER_OF_SENTENCES)]
        start = time.time()
        with ProcessPoolExecutor(max_workers=1) as executor:  # Un worker por size
            futures = [executor.submit(_process_batch, [text], dictionary) for text in texts]
            for future in as_completed(futures):
                pass
        execution_time = time.time() - start
        times.append(execution_time)
        print(f" Tamaño {size}: Ejecución completada en {execution_time:.6f}s")
    # Calculamos
    times_array = np.array(times)
    mean = np.mean(times_array)
    std_dev = np.std(times_array, ddof=1)
    return size, {'mean': mean, 'std_dev': std_dev, 'times': times}

def _process_batch(texts, dictionary):
    """Función auxiliar para procesar un lote de textos."""
    procesar_texto(texts, dictionary)
    return time.time() - time.time()  # Devolvemos un tiempo de ejecución ficticio

def generate_random_dictionary(size, min_length=3, max_length=MAX_WORD_LENGTH):
    """Genera un diccionario aleatorio de palabras."""
    dictionary = []
    for _ in range(size):
        word_length = random.randint(min_length, max_length)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))
        dictionary.append(word)
    return dictionary

def generate_valid_text(dictionary, length):
    """Genera un texto aleatorio usando palabras del diccionario."""
    return ''.join(random.choice(dictionary) for _ in range(length))

# Medición de tiempo con paralelismo (un proceso por tamaño)
def measure_execution_time_parallel(sizes):
    """Mide el tiempo de ejecución para diferentes tamaños de entrada usando paralelismo (un proceso por tamaño)."""
    dictionary_size = 3001  # Tamaño fijo del diccionario
    dictionary = generate_random_dictionary(dictionary_size)
    results = {}
    futures = []
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        for size in sizes:
            future = executor.submit(_process_size, size, RUNS_PER_SIZE, dictionary)
            futures.append(future)
        for future in as_completed(futures):
            size, result = future.result()
            results[size] = result
    return dict(sorted(results.items()))  # Devolvemos los resultados ordenados por tamaño

# Análisis por cuadrados mínimos
def least_squares_analysis(sizes, times):
    """Realiza un análisis de complejidad usando cuadrados mínimos para los modelos lineal, cuadrático, cúbico y a la cuarta."""
    x = np.array(sizes)
    y = np.array(times)

    # Modelo lineal: y = a*x + b
    A_linear = np.vstack([x, np.ones(len(x))]).T
    a_linear, b_linear = np.linalg.lstsq(A_linear, y, rcond=None)[0]
    y_linear = a_linear * x + b_linear
    r2_linear = 1 - np.sum((y - y_linear)**2) / np.sum((y - np.mean(y))**2)

    # Modelo cuadrático: y = a*x^2 + b*x + c
    A_quad = np.vstack([x**2, x, np.ones(len(x))]).T
    a_quad, b_quad, c_quad = np.linalg.lstsq(A_quad, y, rcond=None)[0]
    y_quad = a_quad * x**2 + b_quad * x + c_quad
    r2_quad = 1 - np.sum((y - y_quad)**2) / np.sum((y - np.mean(y))**2)

    # Modelo cúbico: y = a*x^3 + b*x^2 + c*x + d
    A_cubic = np.vstack([x**3, x**2, x, np.ones(len(x))]).T
    a_cubic, b_cubic, c_cubic, d_cubic = np.linalg.lstsq(A_cubic, y, rcond=None)[0]
    y_cubic = a_cubic * x**3 + b_cubic * x**2 + c_cubic * x + d_cubic
    r2_cubic = 1 - np.sum((y - y_cubic)**2) / np.sum((y - np.mean(y))**2)

    # Modelo a la cuarta: y = a*x^4 + b*x^3 + c*x^2 + d*x + e
    A_fourth = np.vstack([x**4, x**3, x**2, x, np.ones(len(x))]).T
    a_fourth, b_fourth, c_fourth, d_fourth, e_fourth = np.linalg.lstsq(A_fourth, y, rcond=None)[0]
    y_fourth = a_fourth * x**4 + b_fourth * x**3 + c_fourth * x**2 + d_fourth * x + e_fourth
    r2_fourth = 1 - np.sum((y - y_fourth)**2) / np.sum((y - np.mean(y))**2)

    models = {
        'Lineal': {
            'params': (a_linear, b_linear),
            'r_squared': r2_linear,
            'formula': f'y = {a_linear:.2e}*x + {b_linear:.2e}'
        },
        'Cuadrático': {
            'params': (a_quad, b_quad, c_quad),
            'r_squared': r2_quad,
            'formula': f'y = {a_quad:.2e}*x^2 + {b_quad:.2e}*x + {c_quad:.2e}'
        },
        'Cúbico': {
            'params': (a_cubic, b_cubic, c_cubic, d_cubic),
            'r_squared': r2_cubic,
            'formula': f'y = {a_cubic:.2e}*x^3 + {b_cubic:.2e}*x^2 + {c_cubic:.2e}*x + {d_cubic:.2e}'
        },
        'Cuarta': {
            'params': (a_fourth, b_fourth, c_fourth, d_fourth, e_fourth),
            'r_squared': r2_fourth,
            'formula': f'y = {a_fourth:.2e}*x^4 + {b_fourth:.2e}*x^3 + {c_fourth:.2e}*x^2 + {d_fourth:.2e}*x + {e_fourth:.2e}'
        }
    }
    return models

# Visualización de resultados
def plot_complexity_results(sizes, results, models):
    """Genera gráficos para visualizar los resultados del análisis de complejidad."""
    fig, ax = plt.subplots(figsize=(10, 6))
    # Datos medidos
    means = [results[size]['mean'] for size in sizes]
    std_devs = [results[size]['std_dev'] for size in sizes]
    # Gráfico de tiempos medidos
    ax.errorbar(sizes, means, yerr=std_devs, fmt='o-', capsize=5, label='Tiempo medido')
    ax.set_title('Tiempo de ejecución vs Tamaño del diccionario')
    ax.set_xlabel('Tamaño del diccionario')
    ax.set_ylabel('Tiempo (s)')
    ax.grid(True)

    # Curva ajustada lineal
    x_fit = np.linspace(min(sizes), max(sizes), 100)
    # linear_model = models['Lineal']
    # a_linear, b_linear = linear_model['params']
    # y_linear_fit = a_linear * x_fit + b_linear
    # ax.plot(x_fit, y_linear_fit, '-.', label=f"Ajuste Lineal (R² = {linear_model['r_squared']:.4f})")

    # # Curva ajustada cuadrática
    # quadratic_model = models['Cuadrático']
    # a_quad, b_quad, c_quad = quadratic_model['params']
    # y_quadratic_fit = a_quad * x_fit**2 + b_quad * x_fit + c_quad
    # ax.plot(x_fit, y_quadratic_fit, ':', label=f"Ajuste Cuadrático (R² = {quadratic_model['r_squared']:.4f})")

    # Curva ajustada cúbica
    cubic_model = models['Cúbico']
    a_cubic, b_cubic, c_cubic, d_cubic = cubic_model['params']
    y_cubic_fit = a_cubic * x_fit**3 + b_cubic * x_fit**2 + c_cubic * x_fit + d_cubic
    ax.plot(x_fit, y_cubic_fit, '--', label=f"Ajuste Cúbico (R² = {cubic_model['r_squared']:.4f})")

    # Curva ajustada a la cuarta
    fourth_model = models['Cuarta']
    a_fourth, b_fourth, c_fourth, d_fourth, e_fourth = fourth_model['params']
    y_fourth_fit = a_fourth * x_fit**4 + b_fourth * x_fit**3 + c_fourth * x_fit**2 + d_fourth * x_fit + e_fourth
    ax.plot(x_fit, y_fourth_fit, '-', label=f"Ajuste Cuarta (R² = {fourth_model['r_squared']:.4f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(f'dictionary_size_complexity_analysis_{sizes[0]}.png', dpi=300)
    plt.show()
# NUEVAS FUNCIONES PARA VARIAR TAMAÑO DEL DICCIONARIO

def generate_fixed_length_dictionary(size):
    """Genera un diccionario de palabras con longitud constante."""
    dictionary = []
    for _ in range(size):
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(FIXED_WORD_LENGTH))
        dictionary.append(word)
    return dictionary

def measure_dictionary_size_complexity(sizes):
    """Mide el tiempo de ejecución variando el tamaño del diccionario."""
    print(f"Analizando el impacto del tamaño del diccionario con palabras de longitud constante {FIXED_WORD_LENGTH}...")
    results = {}
    futures = []

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        for dict_size in sizes:
            future = executor.submit(_process_dictionary_size, dict_size)
            futures.append(future)
        for future in as_completed(futures):
            dict_size, result = future.result()
            results[dict_size] = result

    return dict(sorted(results.items()))

def _process_dictionary_size(dict_size):
    """Mide el tiempo de ejecución para un tamaño específico de diccionario."""
    print(f"Midiendo para diccionario de tamaño {dict_size}...")
    times = []

    for _ in range(RUNS_PER_SIZE):
        # Generamos diccionario con palabras de longitud constante
        dictionary = generate_fixed_length_dictionary(dict_size)

        # Generamos textos usando el diccionario
        texts = [generate_valid_text(dictionary, NUMBER_OF_WORDS_IN_ONE_SENTENCE) for _ in range(NUMBER_OF_SENTENCES)]

        # Medimos tiempo de ejecución
        start = time.time()
        with ProcessPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(_process_batch, [text], dictionary) for text in texts]
            for future in as_completed(futures):
                pass
        execution_time = time.time() - start
        times.append(execution_time)
        print(f" Diccionario tamaño {dict_size}: Ejecución completada en {execution_time:.6f}s")

    # Calculamos estadísticas
    times_array = np.array(times)
    mean = np.mean(times_array)
    std_dev = np.std(times_array, ddof=1)
    return dict_size, {'mean': mean, 'std_dev': std_dev, 'times': times}

def plot_dictionary_size_results(dict_sizes, results, models):
    """Genera gráficos para visualizar los resultados del análisis de complejidad por tamaño de diccionario."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Datos medidos
    means = [results[size]['mean'] for size in dict_sizes]
    std_devs = [results[size]['std_dev'] for size in dict_sizes]

    # Gráfico de tiempos medidos
    ax.errorbar(dict_sizes, means, yerr=std_devs, fmt='o-', capsize=5, label='Tiempo medido')
    ax.set_title(f'Tiempo de ejecución vs Tamaño del diccionario (palabras de longitud {FIXED_WORD_LENGTH})')
    ax.set_xlabel('Tamaño del diccionario')
    ax.set_ylabel('Tiempo (s)')
    ax.grid(True)

    # Curva ajustada cúbica
    x_fit = np.linspace(min(dict_sizes), max(dict_sizes), 100)
    # cubic_model = models['Cúbico']
    # a_cubic, b_cubic, c_cubic, d_cubic = cubic_model['params']
    # y_cubic_fit = a_cubic * x_fit**3 + b_cubic * x_fit**2 + c_cubic * x_fit + d_cubic
    # ax.plot(x_fit, y_cubic_fit, '--', label=f"Ajuste Cúbico (R² = {cubic_model['r_squared']:.4f})")

    # Recta ajustada lineal
    linear_model = models['Lineal']
    a_linear, b_linear = linear_model['params']
    y_linear_fit = a_linear * x_fit + b_linear
    ax.plot(x_fit, y_linear_fit, '-.', label=f"Ajuste Lineal (R² = {linear_model['r_squared']:.4f})")

    # # Curva ajustada cuadrática
    # quadratic_model = models['Cuadrático']
    # a_quad, b_quad, c_quad = quadratic_model['params']
    # y_quadratic_fit = a_quad * x_fit**2 + b_quad * x_fit + c_quad
    # ax.plot(x_fit, y_quadratic_fit, ':', label=f"Ajuste Cuadrático (R² = {quadratic_model['r_squared']:.4f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(f'dictionary_size_analysis_with_fits_{dict_sizes[0]}.png', dpi=300)
    plt.show()

# Función principal para analizar el impacto del tamaño del diccionario
@performance
def analyze_dictionary_size_impact(sizes):
    print(f"Iniciando análisis del impacto del tamaño del diccionario con {RUNS_PER_SIZE} ejecuciones por tamaño...")

    # Medimos los tiempos de ejecución
    results = measure_dictionary_size_complexity(sizes)

    # Preparamos los datos para el análisis
    means = [results[size]['mean'] for size in results]

    # Realizamos el análisis por cuadrados mínimos
    models = least_squares_analysis(list(results.keys()), means)

    # Mostramos los resultados
    print("\nResultados del análisis de complejidad por tamaño de diccionario:")
    print("-" * 60)
    print(f"{'Modelo':<10} {'R²':<10} {'Fórmula'}")
    print("-" * 60)

    for model_name, model_data in models.items():
        print(f"{model_name:<10} {model_data['r_squared']:.6f} {model_data['formula']}")

    # Visualizamos los resultados
    plot_dictionary_size_results(list(results.keys()), results, models)

    return results, models


def analyze_time_complexity():
    """Función para analizar la complejidad temporal del algoritmo."""
    # Tamaños de entrada a probar
    sizes = SIZES_TIME_COMPLEXITY

    print(f"Iniciando análisis de complejidad con paralelismo ({WORKERS} workers) y {RUNS_PER_SIZE} ejecuciones por tamaño...")

    # Medimos los tiempos de ejecución usando paralelismo (un proceso por tamaño)
    results = measure_execution_time_parallel(sizes)

    # Preparamos los datos para el análisis
    means = [results[size]['mean'] for size in results]

    # Realizamos el análisis por cuadrados mínimos
    models = least_squares_analysis(list(results.keys()), means)

    # Mostramos los resultados
    print("\nResultados del análisis de complejidad por cuadrados mínimos:")
    print("-" * 50)
    print(f"{'Modelo':<10} {'R²':<10} {'Fórmula'}")
    print("-" * 50)

    for model_name, model_data in models.items():
        print(f"{model_name:<10} {model_data['r_squared']:.6f} {model_data['formula']}")

    # Visualizamos los resultados
    plot_complexity_results(list(results.keys()), results, models)


# Función principal modificada para usar la versión paralela de la medición
@performance
def main():
    analyze_time_complexity()
    # print("\n\n" + "="*80)

    # print("ANÁLISIS DEL IMPACTO DEL TAMAÑO DEL DICCIONARIO")
    # print("="*80)

    # analyze_dictionary_size_impact(DICTIONARY_SIZES)

    # print("\n\n" + "="*80)

    # global MAX_WORD_LENGTH
    # global FIXED_WORD_LENGTH
    # global NUMBER_OF_WORDS_IN_ONE_SENTENCE

    # MAX_WORD_LENGTH = 40  # Longitud máxima de las palabras
    # NUMBER_OF_WORDS_IN_ONE_SENTENCE = 10  # Tamaño fijo del texto a procesar
    # FIXED_WORD_LENGTH = 10  # Longitud constante para cada palabra del diccionario

    # analyze_dictionary_size_impact(HUGE_DICTIONARY_SIZES)

if __name__ == "__main__":
    main()