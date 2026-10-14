"""Společný vzhled obrázků doplňkových materiálů a jejich ukládání."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")                     # vykreslení bez grafického okna
import matplotlib.pyplot as plt

SLOZKA_GRAFU = Path(__file__).resolve().parent / "graphs"

# paleta Okabe–Ito, rozlišitelná i při poruchách barvocitu
BARVY = {
    "modra": "#0072B2",
    "oranzova": "#E69F00",
    "zelena": "#009E73",
    "cervena": "#D55E00",
    "fialova": "#CC79A7",
    "svetle_modra": "#56B4E9",
    "seda": "#7F7F7F",
}


def nastav_styl() -> None:
    """Nastaví jednotný vzhled všech obrázků."""
    plt.rcParams.update({
        "figure.facecolor": "white",      # bílé pozadí, čitelné i v tmavém režimu GitHubu
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",           # písmo převedeno na křivky, diakritika nezávisí na prohlížeči
        "svg.hashsalt": "doplnkove-materialy",   # stálé identifikátory, výstup je při opakování shodný
    })


def uloz(fig, nazev: str) -> Path:
    """Uloží obrázek jako SVG do složky graphs/ a zavře jej."""
    SLOZKA_GRAFU.mkdir(exist_ok=True)
    cesta = SLOZKA_GRAFU / f"{nazev}.svg"
    fig.savefig(cesta, bbox_inches="tight", metadata={"Date": None})   # bez data, výstup je stálý
    plt.close(fig)
    print(f"uloženo: scripts/graphs/{cesta.name}")
    return cesta
