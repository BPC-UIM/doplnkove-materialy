"""Obrázky k materiálu o kompromisu mezi zkreslením a rozptylem (04-strojove-uceni/bias-variance.md)."""
import matplotlib.pyplot as plt
import numpy as np

from _styl import BARVY, nastav_styl, uloz


def terc() -> None:
    """Terč 2 × 2: kombinace nízkého a vysokého zkreslení a rozptylu."""
    rng = np.random.default_rng(0)
    fig, osy = plt.subplots(2, 2, figsize=(7, 7))
    varianty = [
        (0, 0, 0.0, 0.15, "nízké zkreslení, nízký rozptyl"),
        (0, 1, 0.0, 0.55, "nízké zkreslení, vysoký rozptyl"),
        (1, 0, 0.9, 0.15, "vysoké zkreslení, nízký rozptyl"),
        (1, 1, 0.9, 0.55, "vysoké zkreslení, vysoký rozptyl"),
    ]
    for radek, sloupec, posun, rozptyl, titulek in varianty:
        osa = osy[radek, sloupec]
        for polomer, barva in zip([2.0, 1.5, 1.0, 0.5], ["#f2f2f2", "#d9d9d9", "#bfbfbf", "#a6a6a6"]):
            osa.add_patch(plt.Circle((0, 0), polomer, color=barva, zorder=0))
        stred = np.array([posun, posun * 0.6])           # posun středu = zkreslení
        body = stred + rng.normal(0, rozptyl, size=(12, 2))   # rozptyl kolem středu = rozptyl
        osa.scatter(body[:, 0], body[:, 1], s=28, color=BARVY["cervena"], edgecolor="white", zorder=2)
        osa.plot(0, 0, marker="+", color="black", markersize=12, zorder=3)
        osa.set_xlim(-2.4, 2.4)
        osa.set_ylim(-2.4, 2.4)
        osa.set_aspect("equal")
        osa.axis("off")
        osa.set_title(titulek, fontsize=10)
    fig.suptitle("Body: předpovědi modelů natrénovaných na různých trénovacích množinách\n"
                 "Střed terče (+): skutečná hodnota", fontsize=10, y=0.98)
    uloz(fig, "bias-variance_terc")


def u_krivka() -> None:
    """Rozklad očekávané chyby na zkreslení², rozptyl a šum v závislosti na složitosti."""
    slozitost = np.linspace(0.6, 10, 300)
    zkresleni2 = 6 / slozitost                           # schematický průběh: klesá se složitostí
    rozptyl = 0.06 * slozitost ** 2                      # schematický průběh: roste se složitostí
    sum = np.full_like(slozitost, 0.8)                   # neredukovatelný šum: konstantní
    celkova = zkresleni2 + rozptyl + sum
    i_opt = np.argmin(celkova)

    fig, osa = plt.subplots(figsize=(7.5, 4.5))
    osa.plot(slozitost, zkresleni2, color=BARVY["modra"], label="zkreslení²")
    osa.plot(slozitost, rozptyl, color=BARVY["oranzova"], label="rozptyl")
    osa.plot(slozitost, sum, color=BARVY["seda"], linestyle=":", label="neredukovatelný šum")
    osa.plot(slozitost, celkova, color="black", linewidth=2.2, label="celková chyba")
    osa.axvline(slozitost[i_opt], color=BARVY["zelena"], linestyle="--", linewidth=1)
    osa.annotate("optimum", (slozitost[i_opt], celkova[i_opt]), xytext=(10, 25),
                 textcoords="offset points", color=BARVY["zelena"])
    osa.text(2.6, 10.2, "← nedoučení\n(převažuje zkreslení)", ha="center", fontsize=10)
    osa.text(8.4, 10.2, "přeučení →\n(převažuje rozptyl)", ha="center", fontsize=10)
    osa.set_ylim(0, 11.5)
    osa.set_xlim(slozitost[0], slozitost[-1])
    osa.set_xticks([])
    osa.set_yticks([])
    osa.set_xlabel("složitost modelu")
    osa.set_ylabel("očekávaná chyba")
    osa.legend(loc="upper center", frameon=False, ncol=2, bbox_to_anchor=(0.55, 0.78))
    uloz(fig, "bias-variance_u-krivka")


if __name__ == "__main__":
    nastav_styl()
    terc()
    u_krivka()
