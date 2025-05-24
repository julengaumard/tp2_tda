import numpy as np
import matplotlib.pyplot as plt
import random
import string
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from algoritmo import procesar_texto
from utils import performance

# O(m * (k + (L²) * n))

# Constantes globales para el análisis
SIZES_TIME_COMPLEXITY = [ num for num in range(100, 1000, 100) ]        #(n)
FIXED_DICT_SIZE = 10                                               #(k)
DICTIONARY_SIZES = [ num for num in range(4000, 40_001, 4000) ]
HUGE_DICTIONARY_SIZES = [ num for num in range(10_000, 1_000_000, 50_000) ]
WORD_LENGTHS = [num for num in range(10, 100, 10)]  # Word lengths to test from 3 to 23

MAX_WORD_LENGTH = 23                    # Longitud máxima de las palabras    (L)
NUMBER_OF_WORDS_IN_ONE_SENTENCE = 10   # Tamaño fijo del texto a procesar   (n)
NUMBER_OF_SENTENCES = 3000               # Cantidad de oraciones por caso     (m)

FIXED_WORD_LENGTH = 23  # Longitud constante para cada palabra del diccionario
RUNS_PER_SIZE = 5  # Número de ejecuciones por tamaño

GRAPHS_DIR = "graficosV2/"

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
    dictionary_size = FIXED_DICT_SIZE  # Tamaño fijo del diccionario
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
    # A_linear = np.vstack([x, np.ones(len(x))]).T
    # a_linear, b_linear = np.linalg.lstsq(A_linear, y, rcond=None)[0]
    # y_linear = a_linear * x + b_linear
    # r2_linear = 1 - np.sum((y - y_linear)**2) / np.sum((y - np.mean(y))**2)

    # Modelo cuadrático: y = a*x^2 + b*x + c
    A_quad = np.vstack([x**2, x, np.ones(len(x))]).T
    a_quad, b_quad, c_quad = np.linalg.lstsq(A_quad, y, rcond=None)[0]
    y_quad = a_quad * x**2 + b_quad * x + c_quad
    r2_quad = 1 - np.sum((y - y_quad)**2) / np.sum((y - np.mean(y))**2)

    models = {
        # 'Lineal': {
        #     'params': (a_linear, b_linear),
        #     'r_squared': r2_linear,
        #     'formula': f'y = {a_linear:.2e}*x + {b_linear:.2e}'
        # },
        'Cuadrático': {
            'params': (a_quad, b_quad, c_quad),
            'r_squared': r2_quad,
            'formula': f'y = {a_quad:.2e}*x^2 + {b_quad:.2e}*x + {c_quad:.2e}'
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
    ax.set_title('Tiempo de ejecución vs Tamaño de entrada')
    ax.set_xlabel('Tamaño de entrada')
    ax.set_ylabel('Tiempo (s)')
    ax.grid(True)

    x_fit = np.linspace(min(sizes), max(sizes), 100)
    linear_model = models['Lineal']
    a_linear, b_linear = linear_model['params']
    y_linear_fit = a_linear * x_fit + b_linear
    ax.plot(x_fit, y_linear_fit, '-.', label=f"Ajuste Lineal (R² = {linear_model['r_squared']:.4f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{GRAPHS_DIR}dictionary_size_complexity_analysis_{sizes[0]}.png', dpi=300)
    plt.show()


def generate_fixed_length_dictionary(size, word_length):
    """Genera un diccionario de palabras con longitud constante."""
    dictionary = []
    for _ in range(size):
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))
        dictionary.append(word)
    return dictionary

def _process_word_length(word_length):
    """Mide el tiempo de ejecución para una longitud específica de palabra."""
    print(f"Midiendo para longitud de palabra {word_length}...")
    times = []

    for _ in range(RUNS_PER_SIZE):
        # Generamos diccionario con palabras de longitud constante
        dictionary = generate_fixed_length_dictionary(FIXED_DICT_SIZE, word_length)

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
        print(f" Longitud {word_length}: Ejecución completada en {execution_time:.6f}s")

    # Calculamos estadísticas
    times_array = np.array(times)
    mean = np.mean(times_array)
    std_dev = np.std(times_array, ddof=1)
    return word_length, {'mean': mean, 'std_dev': std_dev, 'times': times}

def measure_word_length_complexity(lengths):
    """Mide el tiempo de ejecución variando la longitud de las palabras."""
    print(f"Analizando el impacto de la longitud de las palabras con diccionario de tamaño fijo {FIXED_DICT_SIZE}...")
    results = {}
    futures = []

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        for length in lengths:
            future = executor.submit(_process_word_length, length)
            futures.append(future)
        for future in as_completed(futures):
            length, result = future.result()
            results[length] = result

    return dict(sorted(results.items()))

def plot_word_length_results(lengths, results, models):
    """Genera gráficos para visualizar los resultados del análisis de complejidad por longitud de palabra."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Datos medidos
    means = [results[length]['mean'] for length in lengths]
    std_devs = [results[length]['std_dev'] for length in lengths]

    # Gráfico de tiempos medidos
    ax.errorbar(lengths, means, yerr=std_devs, fmt='o-', capsize=5, label='Tiempo medido')
    ax.set_title(f'Tiempo de ejecución vs Longitud de palabra (diccionario de tamaño {FIXED_DICT_SIZE})')
    ax.set_xlabel('Longitud de palabra')
    ax.set_ylabel('Tiempo (s)')
    ax.grid(True)

    # Curva ajustada
    x_fit = np.linspace(min(lengths), max(lengths), 100)

    # Recta ajustada lineal
    # linear_model = models['Lineal']
    # a_linear, b_linear = linear_model['params']
    # y_linear_fit = a_linear * x_fit + b_linear
    # ax.plot(x_fit, y_linear_fit, '-.', label=f"Ajuste Lineal (R² = {linear_model['r_squared']:.4f})")

    # Curva ajustada cuadrática
    quadratic_model = models['Cuadrático']
    a_quad, b_quad, c_quad = quadratic_model['params']
    y_quadratic_fit = a_quad * x_fit**2 + b_quad * x_fit + c_quad
    ax.plot(x_fit, y_quadratic_fit, ':', label=f"Ajuste Cuadrático (R² = {quadratic_model['r_squared']:.4f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{GRAPHS_DIR}word_length_analysis_{lengths[0]}.png', dpi=300)
    plt.show()

def analyze_word_length_impact(lengths):
    print(f"Iniciando análisis del impacto de la longitud de palabra con {RUNS_PER_SIZE} ejecuciones por longitud...")

    # Medimos los tiempos de ejecución
    results = measure_word_length_complexity(lengths)

    # Preparamos los datos para el análisis
    means = [results[length]['mean'] for length in results]

    # Realizamos el análisis por cuadrados mínimos
    models = least_squares_analysis(list(results.keys()), means)

    # Mostramos los resultados
    print("\nResultados del análisis de complejidad por longitud de palabra:")
    print("-" * 60)
    print(f"{'Modelo':<10} {'R²':<10} {'Fórmula'}")
    print("-" * 60)

    for model_name, model_data in models.items():
        print(f"{model_name:<10} {model_data['r_squared']:.6f} {model_data['formula']}")

    # Visualizamos los resultados
    plot_word_length_results(list(results.keys()), results, models)

    return results, models

def analyze_dictionary_size_impact(sizes):
    print(f"Iniciando análisis del impacto del tamaño del diccionario con {RUNS_PER_SIZE} ejecuciones por tamaño...")

    # Medimos los tiempos de ejecución
    results = measure_execution_time_parallel(sizes)

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
    plot_complexity_results(list(results.keys()), results, models)

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
    # analyze_time_complexity()
    # print("\n\n" + "="*80)

    # print("ANÁLISIS DEL IMPACTO DEL TAMAÑO DEL DICCIONARIO")
    # print("="*80)

    # analyze_dictionary_size_impact(DICTIONARY_SIZES)

    # print("\n\n" + "="*80)

    # print("ANÁLISIS DEL IMPACTO DE LA LONGITUD DE PALABRA")
    # print("="*80)

    analyze_word_length_impact(WORD_LENGTHS)

    print("\n\n" + "="*80)

#    global FIXED_WORD_LENGTH
#    global NUMBER_OF_WORDS_IN_ONE_SENTENCE

#    NUMBER_OF_WORDS_IN_ONE_SENTENCE = 10
#    FIXED_WORD_LENGTH = 23

    # analyze_dictionary_size_impact(HUGE_DICTIONARY_SIZES)

if __name__ == "__main__":
    main()