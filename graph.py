import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Datos
x = np.array([100, 200, 300, 400, 500, 600, 1000, 2000])
y = np.array([10.556860, 42.026719, 107.529630, 213.332054, 366.279001, 576.435760, 2173.240080, 14349.304922])

# Ajustes polinomiales
poly1 = np.polyfit(x, y, 1)  # Lineal
poly2 = np.polyfit(x, y, 2)  # Cuadrático
poly3 = np.polyfit(x, y, 3)  # Cúbico

# Ajuste exponencial: y = a * exp(b * x) -> log(y) = log(a) + b * x
log_y = np.log(y)
exp_coef = np.polyfit(x, log_y, 1)
a_exp, b_exp = np.exp(exp_coef[1]), exp_coef[0]

# Predicciones
x_fit = np.linspace(min(x), max(x), 500)
y_pred_poly1 = np.polyval(poly1, x_fit)
y_pred_poly2 = np.polyval(poly2, x_fit)
y_pred_poly3 = np.polyval(poly3, x_fit)
y_pred_exp = a_exp * np.exp(b_exp * x_fit)

# Errores cuadráticos medios
mse_poly1 = mean_squared_error(y, np.polyval(poly1, x))
mse_poly2 = mean_squared_error(y, np.polyval(poly2, x))
mse_poly3 = mean_squared_error(y, np.polyval(poly3, x))
mse_exp = mean_squared_error(y, a_exp * np.exp(b_exp * x))

# Graficar
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='black', label='Datos originales')
plt.plot(x_fit, y_pred_poly1, label=f'Lineal (MSE={mse_poly1:.1f})', linestyle='--')
plt.plot(x_fit, y_pred_poly2, label=f'Cuadrático (MSE={mse_poly2:.1f})', linestyle='-.')
plt.plot(x_fit, y_pred_poly3, label=f'Cúbico (MSE={mse_poly3:.1f})', linestyle=':')
plt.plot(x_fit, y_pred_exp, label=f'Exponencial (MSE={mse_exp:.1f})', linestyle='-')

plt.title('Ajuste por cuadrados mínimos')
plt.xlabel('Tamaño')
plt.ylabel('Tiempo (s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
