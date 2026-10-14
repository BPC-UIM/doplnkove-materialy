"""Obrázky k materiálu o profilování a výkonu (02-overovani-a-ladeni/profilovani-vykon.md)."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from _styl import BARVY, nastav_styl, uloz


def tridy_slozitosti() -> None:
    """Výstup příkladu z kapitoly 7 materiálu (kód je s příkladem shodný)."""
    tridy = {
        "O(1)":       lambda n: np.ones_like(n),
        "O(log n)":   lambda n: np.log2(n),
        "O(n)":       lambda n: n,
        "O(n log n)": lambda n: n * np.log2(n),
        "O(n^2)":     lambda n: n ** 2,
        "O(2^n)":     lambda n: 2.0 ** n,
    }

    fig, (vlevo, vpravo) = plt.subplots(1, 2, figsize=(12, 4.5))

    n_male = np.linspace(1, 6, 500)
    for nazev, f in tridy.items():
        vlevo.plot(n_male, f(n_male), label=nazev)
    vlevo.set_title("Malé vstupy: křivky se kříží")
    vlevo.set_xlabel("velikost vstupu n")
    vlevo.set_ylabel("počet operací")
    vlevo.grid()
    vlevo.legend()

    n_velke = np.linspace(2, 40, 500)
    for nazev, f in tridy.items():
        vpravo.plot(n_velke, f(n_velke), label=nazev)
    vpravo.set_yscale("log")
    vpravo.set_title("Větší vstupy (log. osa y): pořadí tříd je zřejmé")
    vpravo.set_xlabel("velikost vstupu n")
    vpravo.set_ylabel("počet operací (log)")
    vpravo.grid(which="both", alpha=0.4)
    vpravo.legend()

    plt.tight_layout()
    uloz(fig, "profilovani_tridy-slozitosti")


def _matice(osa, x0, y0, hodnoty, barva, virtualni=None, popisek=None):
    """Vykreslí pole jako mřížku buněk; buňky v masce `virtualni` jsou pouze rozšířené (bez kopie dat)."""
    radku, sloupcu = hodnoty.shape
    for r in range(radku):
        for s in range(sloupcu):
            rozsirena = virtualni is not None and virtualni[r, s]
            osa.add_patch(Rectangle(
                (x0 + s, y0 - r - 1), 1, 1,
                facecolor="white" if rozsirena else barva,
                edgecolor=barva if rozsirena else "black",
                linestyle="--" if rozsirena else "-",
                hatch="//" if rozsirena else None,
                linewidth=1.0,
            ))
            osa.text(x0 + s + 0.5, y0 - r - 0.5, f"{hodnoty[r, s]:g}", ha="center", va="center",
                     fontsize=10, color=BARVY["seda"] if rozsirena else "black")
    if popisek:
        osa.text(x0 + sloupcu / 2, y0 + 0.35, popisek, ha="center", va="bottom", fontsize=10)


def broadcasting() -> None:
    """Rozšíření rozměrů velikosti 1 při operaci mezi poli různého tvaru."""
    fig, (horni, dolni) = plt.subplots(2, 1, figsize=(8, 6.6))

    # (3, 2) − (2,): průměr sloupců se rozšíří na všechny řádky
    X = np.array([[1.0, 200.0], [2.0, 300.0], [3.0, 400.0]])
    prumer = X.mean(axis=0)
    prumer_rozsireny = np.tile(prumer, (3, 1))
    maska = np.zeros((3, 2), dtype=bool)
    maska[1:, :] = True
    _matice(horni, 0, 0, X, BARVY["svetle_modra"], popisek="X, tvar (3, 2)")
    horni.text(2.75, -1.5, "−", fontsize=18, ha="center", va="center")
    _matice(horni, 3.5, 0, prumer_rozsireny, BARVY["oranzova"], virtualni=maska, popisek="prumer, tvar (2,) → (3, 2)")
    horni.text(6.25, -1.5, "=", fontsize=18, ha="center", va="center")
    _matice(horni, 7, 0, X - prumer, BARVY["zelena"], popisek="výsledek, tvar (3, 2)")
    horni.set_xlim(-0.3, 9.3)
    horni.set_ylim(-3.3, 1.0)

    # (4, 1) − (1, 3): sloupec i řádek se rozšíří na tvar (4, 3)
    a = np.array([[0.0], [10.0], [20.0], [30.0]])
    b = np.array([[1.0, 2.0, 3.0]])
    a_rozsirene = np.tile(a, (1, 3))
    b_rozsirene = np.tile(b, (4, 1))
    maska_a = np.zeros((4, 3), dtype=bool)
    maska_a[:, 1:] = True
    maska_b = np.zeros((4, 3), dtype=bool)
    maska_b[1:, :] = True
    _matice(dolni, 0, 0, a_rozsirene, BARVY["svetle_modra"], virtualni=maska_a, popisek="a, tvar (4, 1) → (4, 3)")
    dolni.text(3.5, -2, "−", fontsize=18, ha="center", va="center")
    _matice(dolni, 4, 0, b_rozsirene, BARVY["oranzova"], virtualni=maska_b, popisek="b, tvar (1, 3) → (4, 3)")
    dolni.text(7.5, -2, "=", fontsize=18, ha="center", va="center")
    _matice(dolni, 8, 0, a - b, BARVY["zelena"], popisek="výsledek, tvar (4, 3)")
    dolni.set_xlim(-0.3, 11.3)
    dolni.set_ylim(-4.3, 1.0)

    for osa in (horni, dolni):
        osa.set_aspect("equal")
        osa.axis("off")
    fig.text(0.5, 0.02, "Plné buňky: data uložená v paměti.   Šrafované buňky: rozšíření rozměru velikosti 1, data se nekopírují.",
             ha="center", fontsize=9, color=BARVY["seda"])
    uloz(fig, "profilovani_broadcasting")


def ulozeni_v_pameti() -> None:
    """Uložení matice 3 × 4 v paměti po řádcích (C-order) a po sloupcích (Fortran-order)."""
    A = np.arange(12).reshape(3, 4)
    barvy_radku = [BARVY["svetle_modra"], BARVY["oranzova"], BARVY["zelena"]]
    fig, osa = plt.subplots(figsize=(10, 5.2))

    # matice; barva buňky odpovídá řádku
    for r in range(3):
        for s in range(4):
            osa.add_patch(Rectangle((s, -r - 1), 1, 1, facecolor=barvy_radku[r], edgecolor="black"))
            osa.text(s + 0.5, -r - 0.5, str(A[r, s]), ha="center", va="center")
    osa.text(2, 0.3, "matice A, tvar (3, 4)", ha="center", va="bottom")

    def pas(y, poradi, titulek, kroky):
        for i, hodnota in enumerate(poradi):
            r = hodnota // 4
            osa.add_patch(Rectangle((i, y), 1, 1, facecolor=barvy_radku[r], edgecolor="black"))
            osa.text(i + 0.5, y + 0.5, str(hodnota), ha="center", va="center")
        osa.text(0, y + 1.25, titulek, ha="left", va="bottom")
        osa.text(12.3, y + 0.5, kroky, ha="left", va="center", fontsize=9, color=BARVY["seda"])

    pas(-5.0, A.flatten(order="C"), "uložení po řádcích (C-order, výchozí v NumPy)",
        f"strides {np.zeros((3, 4)).strides}:\nřádek o 32 B, sloupec o 8 B")
    pas(-7.6, A.flatten(order="F"), "uložení po sloupcích (Fortran-order)",
        f"strides {np.asfortranarray(np.zeros((3, 4))).strides}:\nřádek o 8 B, sloupec o 32 B")
    osa.text(0, -8.6, "Posloupnost buněk zleva doprava odpovídá pořadí v paměti; barva označuje řádek matice (prvky typu float64, 8 B).",
             fontsize=9, color=BARVY["seda"], va="top")

    osa.set_xlim(-0.2, 15.5)
    osa.set_ylim(-9.2, 1.0)
    osa.set_aspect("equal")
    osa.axis("off")
    uloz(fig, "profilovani_ulozeni-v-pameti")


if __name__ == "__main__":
    nastav_styl()
    tridy_slozitosti()
    broadcasting()
    ulozeni_v_pameti()
