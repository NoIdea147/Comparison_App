import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

nutzungsdauer = 30
routine_wartung_motor_kosten = 250

# Definieren Sie Symbole
x = sp.symbols('x')

# Definieren Sie die exponentiellen Funktionen
def exponential_function1(x):
    return 0.02 * sp.exp(-0.55 * x) + 0.01  # Abnahme

def exponential_function2(x):
    return 0.01 * sp.exp(0.2 * (x - 20)) + 0.01

def ausfalls_wartung_motor(x):
    condition = sp.LessThan(x, 6.2)
    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

# Berechnen Sie das bestimmte Integral von 0 bis 30
integral_result = sp.integrate(ausfalls_wartung_motor(x), (x, 0, nutzungsdauer)).evalf()

# Multiplizieren Sie das Integralergebnis mit den Routine-Wartungskosten
gesamtkosten = routine_wartung_motor_kosten * nutzungsdauer + integral_result * 2000*100

print(f"Gesamtkosten: {gesamtkosten}")

# Plot erstellen (optional)
x_values = np.linspace(0, nutzungsdauer, 1000)
y_values = np.vectorize(lambda x: ausfalls_wartung_motor(x).evalf())(x_values)

plt.plot(x_values, y_values)
plt.xlabel('Nutzungsdauer (Jahre)')
plt.ylabel('Wartungskosten')
plt.title('Wartungskosten für Elektrik (SymPy)')
plt.show()
