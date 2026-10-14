"""Obrázky k materiálu o optimalizátorech (04-strojove-uceni/optimalizatory.md).

Předpisy aktualizace odpovídají kapitolám 2, 3 a 6 materiálu.
"""
import matplotlib.pyplot as plt
import numpy as np

from _styl import BARVY, nastav_styl, uloz

# protáhlé údolí: ztrátová funkce je strmá ve směru y a plochá ve směru x
A, B = 0.05, 2.0


def ztrata(x, y):
    return A * x ** 2 + B * y ** 2


def gradient(theta):
    return np.array([2 * A * theta[0], 2 * B * theta[1]])


def gradientni_sestup(theta, eta, kroky):
    draha = [theta.copy()]
    for _ in range(kroky):
        theta = theta - eta * gradient(theta)
        draha.append(theta.copy())
    return np.array(draha)


def moment(theta, eta, beta, kroky):
    m = np.zeros_like(theta)
    draha = [theta.copy()]
    for _ in range(kroky):
        m = beta * m + gradient(theta)
        theta = theta - eta * m
        draha.append(theta.copy())
    return np.array(draha)


def adam(theta, eta, beta1, beta2, kroky, eps=1e-8):
    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    draha = [theta.copy()]
    for t in range(1, kroky + 1):
        g = gradient(theta)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g ** 2
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        theta = theta - eta * m_hat / (np.sqrt(v_hat) + eps)
        draha.append(theta.copy())
    return np.array(draha)


def trajektorie() -> None:
    """Dráhy gradientního sestupu, sestupu s momentem a Adamu v protáhlém údolí."""
    start = np.array([-9.0, 2.0])
    kroky = 40
    drahy = {
        "gradientní sestup (η = 0,45)": (gradientni_sestup(start, 0.45, kroky), BARVY["cervena"]),
        "sestup s momentem (η = 0,2, β = 0,7)": (moment(start, 0.2, 0.7, kroky), BARVY["modra"]),
        "Adam (η = 0,3)": (adam(start, 0.3, 0.9, 0.999, kroky), BARVY["zelena"]),
    }

    x, y = np.meshgrid(np.linspace(-10, 2, 300), np.linspace(-2.6, 2.6, 300))
    fig, osa = plt.subplots(figsize=(8, 4.2))
    osa.contour(x, y, ztrata(x, y), levels=np.geomspace(0.05, 15, 12), colors="#bfbfbf", linewidths=0.8)
    for popisek, (draha, barva) in drahy.items():
        osa.plot(draha[:, 0], draha[:, 1], marker="o", markersize=3, linewidth=1.2, color=barva, label=popisek)
    osa.plot(*start, marker="s", color="black", markersize=6)
    osa.annotate("start", start, xytext=(6, 6), textcoords="offset points")
    osa.plot(0, 0, marker="*", color="black", markersize=12)
    osa.annotate("minimum", (0, 0), xytext=(6, -14), textcoords="offset points")
    osa.set_xlabel("parametr θ₁ (plochý směr)")
    osa.set_ylabel("parametr θ₂ (strmý směr)")
    osa.set_title(f"Prvních {kroky} kroků z téhož počátečního bodu", fontsize=10)
    osa.legend(loc="lower right", frameon=True, fontsize=9)
    uloz(fig, "optimalizatory_trajektorie")


if __name__ == "__main__":
    nastav_styl()
    trajektorie()
