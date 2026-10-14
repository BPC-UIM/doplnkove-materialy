# Reprodukovatelnost a nastavení seedů

*Výukový materiál — zvládnutí náhodnosti v kódu strojového učení*

## 1. Proč na reprodukovatelnosti záleží

Kód ve strojovém učení obsahuje na mnoha místech náhodu. Důsledkem je, že dvojí spuštění téhož programu může vést k odlišným výsledkům. To komplikuje tři základní činnosti:

- **ověřitelnost** — výsledek, který nelze zopakovat, nelze ani spolehlivě obhájit ani zkontrolovat,
- **ladění** — chybu, která se objevuje jen občas, je bez opakovatelného běhu obtížné najít,
- **srovnávání** — mění-li se výsledek mezi spuštěními, nelze rozlišit, zda je rozdíl mezi dvěma modely skutečný, nebo jen náhodný.

Cílem **reprodukovatelnosti** je zajistit, aby opakované spuštění za stejných podmínek vedlo ke stejnému výsledku. Nástrojem k tomu je řízení náhody prostřednictvím tzv. seedů.

## 2. Co je seed

Počítač negeneruje skutečně náhodná čísla, nýbrž tzv. **pseudonáhodná**: generátor je deterministická funkce, která z výchozího stavu vytváří posloupnost čísel, jež se náhodně tváří. Tímto výchozím stavem je **seed** (počáteční hodnota).

Klíčová vlastnost: **stejný seed vede vždy k téže posloupnosti.** Nastavením seedu tedy náhodu nevypínáme — pouze zajišťujeme, že bude pokaždé stejná.

```python
import random

random.seed(42)
print(random.random(), random.random())   # vždy stejná dvojice čísel
```

> Hodnota `42` v příkladech nemá žádný zvláštní význam; seedem může být libovolné celé číslo. Podstatné je, že je zvolen a zaznamenán (viz kapitola 7).

## 3. Kde všude se v ML skrývá náhoda

Náhoda ve strojovém učení nevzniká pouze na jednom místě. Typicky se objevuje při:

- **inicializaci parametrů** modelu (počáteční váhy),
- **míchání dat** (shuffle) před trénováním,
- **rozdělení dat** na trénovací a testovací množinu,
- **regularizaci** typu dropout,
- **rozšiřování dat** (augmentace),
- **vzorkování** (výběr dávek, náhodné podmnožiny).

Zapomenutí byť jediného z těchto míst stačí k tomu, aby výsledek přestal být reprodukovatelný.

## 4. Více generátorů znamená více seedů

Zásadní a často opomíjená skutečnost: v typickém projektu strojového učení nepracuje **jediný** generátor náhody, nýbrž několik nezávislých, každý s vlastním stavem. Nastavení seedu jednoho z nich neovlivní ostatní. Je proto nutné nastavit seed **u všech** použitých generátorů:

```python
import os
import random
import numpy as np
import torch

def nastav_seed(seed: int = 42) -> None:
    random.seed(seed)                      # standardní knihovna
    np.random.seed(seed)                   # NumPy (globální generátor)
    torch.manual_seed(seed)                # PyTorch (CPU)
    torch.cuda.manual_seed_all(seed)       # PyTorch (všechny GPU)
```

V prostředí TensorFlow se seed nastavuje obdobně:

```python
import tensorflow as tf
tf.random.set_seed(42)
```

Kromě knihoven ovlivňuje reprodukovatelnost i **randomizace hašování** v samotném Pythonu, která může měnit pořadí prvků v některých datových strukturách. Ta se řídí proměnnou prostředí, jež musí být nastavena **před** spuštěním interpretu:

```bash
export PYTHONHASHSEED=0
```

## 5. Globální versus lokální generátor

Volání jako `np.random.seed(42)` nastavuje **globální** generátor — jediný stav sdílený celým programem. To je křehké: kterékoli volání knihovny, které si vyžádá náhodné číslo, tento stav posune, a další výsledky se tím změní. Chyba tohoto druhu se hledá velmi obtížně.

Doporučeným přístupem je proto **lokální generátor**, jehož stav je oddělený a předává se výslovně tam, kde je potřeba. V knihovně NumPy:

```python
rng = np.random.default_rng(42)            # samostatný, izolovaný generátor
vyber = rng.integers(0, 100, size=5)
```

V knihovně scikit-learn slouží témuž účelu parametr `random_state`, který je vhodné vždy uvádět výslovně, místo spoléhání na globální stav:

```python
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, random_state=42)
```

> **Doporučení:** Preferujte lokální generátory a výslovné předávání seedu před globálním stavem — ze stejného důvodu, z jakého se v konfiguraci nedoporučuje spoléhat na globální měnitelný stav. Program je pak předvídatelnější a snáze laditelný.

## 6. Nastavený seed ještě nezaručuje determinismus

Toto je nejdůležitější poznatek celého materiálu. Nastavení všech seedů zajistí opakovatelnost pouze potud, pokud jsou i všechny výpočty samy o sobě deterministické. To však neplatí vždy.

> **Upozornění:** I při korektně nastavených seedech se výsledky mohou mezi běhy lišit. Nejčastější příčiny jsou:
> - **výpočty na GPU** — některé operace nemají deterministickou implementaci,
> - **paralelismus** — při souběžném zpracování závisí výsledek na pořadí, v němž se dílčí operace s plovoucí čárkou sečtou,
> - **paralelní načítání dat** — každý pracovní proces (worker) má vlastní generátor, který je nutné zvlášť seedovat,
> - **volba algoritmu kvůli rychlosti** — knihovna může za běhu zvolit rychlejší, avšak nedeterministickou variantu.

Je proto užitečné rozlišovat **úrovně reprodukovatelnosti**:

1. stejný výsledek při opakovaném spuštění **na témže stroji**,
2. stejný výsledek **napříč různými stroji** a hardwarem,
3. **bitově identický** výsledek.

Vyšší úroveň je náročnější a má svou cenu. Vynucení plného determinismu (v PyTorchi například `torch.use_deterministic_algorithms(True)` spolu s `torch.backends.cudnn.benchmark = False`) může výpočet zpomalit, případně skončit chybou u operací, které deterministickou variantu nemají. Pro většinu praktických účelů postačuje první úroveň; plný determinismus se vyžaduje jen tam, kde je skutečně nezbytný.

## 7. Reprodukovatelnost jako výzkumná poctivost

Řízení náhody nesměřuje jen k technické opakovatelnosti, nýbrž i k poctivosti výsledků. S tím souvisí dvě zásady:

- **Seed se nevybírá podle výsledku.** Vyzkoušet mnoho seedů a uvést pouze ten s nejpříznivějším výsledkem je forma sebeklamu — vykazovaný výsledek pak neodráží skutečnou kvalitu modelu, nýbrž šťastnou náhodu. Tento postup je metodologicky nepřípustný.
- **Výsledek se vykazuje přes více seedů.** Namísto jediného čísla je vhodné model spustit s několika různými seedy (typicky třemi až pěti) a uvést průměr spolu s mírou rozptylu. Teprve to vypovídá o tom, nakolik je výsledek stabilní a na náhodě nezávislý.

Pevně zvolený seed tedy slouží k **opakovatelnosti konkrétního běhu**, kdežto hodnocení přes více seedů slouží k **ověření robustnosti** výsledku. Obě role je třeba rozlišovat.

## 8. Zaznamenání seedu a prostředí

Reprodukovatelnost není vlastností jediného řádku kódu, nýbrž celého záznamu podmínek experimentu. K jeho zopakování je nutné znát:

- **použitý seed** — patří mezi konfigurační parametry projektu, a je tedy vhodné jej uvádět v konfiguračním souboru, nikoli jej „zadrátovat" do kódu,
- **verze knihoven** — odlišná verze může vést k odlišnému výsledku i při stejném seedu, proto je nutné verze zafixovat (viz reprodukovatelnost prostředí).

Seed je tedy typický konfigurovatelný parametr; jeho začlenění do konfigurace zároveň zajistí, že bude spolu s ostatními parametry experimentu zaznamenán.

## 9. Doporučený postup

Na začátku programu nastavte seed **u všech** použitých generátorů (standardní knihovna, NumPy, framework). Tam, kde je to možné, upřednostněte **lokální generátory** a výslovné předávání seedu před globálním stavem. Mějte na paměti, že seed zajišťuje opakovatelnost, **nikoli nutně plný determinismus** — vyšší úroveň determinismu vynucujte pouze tehdy, je-li skutečně potřeba. Konečný výsledek vykazujte **přes více seedů** a použitý seed i verze prostředí vždy zaznamenejte.
