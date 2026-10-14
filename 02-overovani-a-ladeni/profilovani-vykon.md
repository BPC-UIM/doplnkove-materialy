# Profilování a výkon

*Výukový materiál — jak odhalit nevýkonný kód a jak jej zrychlit*

Tento materiál má dvě části. První učí **odhalit**, kde je kód pomalý — tedy měřit, nikoli hádat. Druhá shromažďuje **postupy, jak kód zrychlit**, seřazené podle dopadu. Pořadí částí je záměrné a vyjadřuje ústřední zásadu: bez měření se neoptimalizuje.

---

# Část A — Jak odhalit nevýkonný kód

## 1. Nejdřív správně, pak rychle

Optimalizace má pevné pořadí priorit: kód musí **nejprve fungovat správně**, teprve poté je namístě řešit jeho rychlost — a i tehdy pouze tam, kde to měření odůvodní. Předčasná optimalizace (úprava rychlosti dříve, než je známo, kde se čas skutečně tráví) je běžnou chybou: vede ke zbytečně složitému a hůře čitelnému kódu bez prokazatelného přínosu.

Optimalizace má přitom svou cenu — zrychlený kód bývá méně čitelný a hůře udržovatelný. Tato cena je přijatelná jen tam, kde přináší měřitelné zrychlení na místě, které skutečně prodlužuje dobu běhu. Na ostatních místech má přednost čitelnost.

> **Zásada:** Bez měření se neoptimalizuje. Dojem, že je určité místo pomalé, je nespolehlivý; rozhoduje údaj z profileru (kapitola 4).

## 2. Strategický postup

Optimalizace probíhá v opakovaném cyklu:

1. **Změřit výchozí stav (baseline).** Zaznamenat dobu běhu před jakoukoli úpravou, aby bylo vůči čemu poměřovat.
2. **Najít úzké hrdlo.** Profilerem zjistit, které místo spotřebovává nejvíce času. Zpravidla platí, že malá část kódu zabírá většinu doby běhu.
3. **Upravit pouze úzké hrdlo.** Optimalizovat místo, které měření označilo, nikoli to, které se jeví podezřele.
4. **Ověřit správnost.** Po úpravě potvrdit, že výsledek zůstal **nezměněný** — optimalizace, která změní výstup, je chyba. K tomu slouží test pokrývající daný případ (viz [materiál o testování](testovani.md)).
5. **Změřit znovu a porovnat.** Ověřit, že úprava skutečně pomohla, a o kolik.

### Amdahlův zákon: proč záleží na výběru místa

Zrychlení celého programu je omezeno tím, jak velkou část doby běhu dané místo zabírá. Zabírá-li určitá část 5 % celkového času, pak i její nekonečné zrychlení zkrátí celkovou dobu nejvýše o těchto 5 %. Naopak zrychlení části, která zabírá 90 % času, má zásadní dopad. Z toho plyne praktický důsledek: **optimalizace přináší užitek jen tam, kde se tráví podstatná část času** — a právě to ukáže profiler.

## 3. Měření času

Nejjednodušším měřením je doba běhu úseku kódu. K přesnému měření krátkých úseků slouží modul `timeit`, který úsek opakovaně spustí a potlačí náhodné výkyvy. Následující příklad porovnává dva způsoby spojení řetězců a je možné jej vložit do notebooku a spustit:

```python
import timeit

setup = "slova = [str(i) for i in range(1000)]"

cyklus = timeit.timeit("s = ''\nfor w in slova:\n    s += w", setup=setup, number=5000)
spojeni = timeit.timeit("''.join(slova)", setup=setup, number=5000)

print(f"spojování v cyklu: {cyklus:.3f} s")
print(f"metoda join:       {spojeni:.3f} s")
```

Výstup ukáže, že metoda `join` je výrazně rychlejší než opakované spojování v cyklu (kapitola 12).

Zásady spolehlivého měření:

- **Opakovat a zprůměrovat** — jednotlivé měření kolísá; `timeit` proto úsek spouští mnohokrát (parametr `number`).
- **Zahřátí.** První spuštění bývá pomalejší (načtení do paměti, příprava). Pro srovnání se používají až ustálené hodnoty.
- **Nástěnný versus procesorový čas.** Nástěnný čas (wall time) zahrnuje i čekání (na disk, na síť); procesorový čas měří jen výpočet. Pro výpočetní úlohy jsou relevantní oba, u čekání na vstupy a výstupy je rozdíl podstatný.

V prostředí Jupyter je k dispozici magický příkaz `%timeit` (pro jeden řádek) a `%%timeit` (pro celou buňku), který měření zjednodušuje.

## 4. Profilery

Měření jednoho úseku nestačí k nalezení úzkého hrdla v celém programu. K tomu slouží **profiler**, který změří dobu strávenou v jednotlivých funkcích.

### cProfile — kde se tráví čas

Modul `cProfile` je součástí standardní knihovny a vypíše, kolik času připadá na každou funkci:

```python
import cProfile

def pomala_cast():
    return sum(i * i for i in range(1_000_000))

def rychla_cast():
    return sum(range(1000))

def program():
    pomala_cast()
    rychla_cast()

cProfile.run("program()", sort="cumulative")
```

Ve výpisu je u každé funkce počet volání (`ncalls`), vlastní čas (`tottime`) a souhrnný čas včetně volaných funkcí (`cumtime`). Nejvyšší hodnota `cumtime` ukazuje úzké hrdlo. Výstup lze vizualizovat nástrojem `snakeviz`.

### line_profiler — po jednotlivých řádcích

Potřebuje-li se zjistit, který **řádek** funkce je pomalý, slouží k tomu `line_profiler` (instaluje se zvlášť). Funkce se označí dekorátorem `@profile` a spustí nástrojem `kernprof`; výstup uvádí čas připadající na každý řádek.

### Paměť

Spotřebu paměti měří modul `tracemalloc` ze standardní knihovny, který zaznamená, kde se alokuje nejvíce paměti:

```python
import tracemalloc

tracemalloc.start()
data = [i ** 2 for i in range(1_000_000)]
aktualni, vrchol = tracemalloc.get_traced_memory()
print(f"aktuální: {aktualni / 1e6:.1f} MB, vrchol: {vrchol / 1e6:.1f} MB")
tracemalloc.stop()
```

### Profilery pro běžící a vzdálené procesy

Dosud uvedené nástroje vyžadují úpravu či zvláštní spuštění programu. Pro **již běžící** proces — typicky dlouhý trénink na vzdáleném serveru — slouží **vzorkovací profilery**, které proces pouze pozorují zvenčí, aniž by jej bylo nutné upravit:

- **`py-spy`** se připojí k běžícímu procesu podle jeho identifikátoru a průběžně vzorkuje, kde se program nachází; má nízkou režii a nevyžaduje zásah do kódu.
- **`scalene`** měří současně procesor, paměť i využití grafické karty.

## 5. Profilování v kontextu strojového učení a PyTorche

U tréninku modelů je nejčastější otázkou, zda je úzkým hrdlem **načítání dat**, nebo **výpočet na grafické kartě**. Obojí se odhalí odlišně:

- **Využití grafické karty** ukáže příkaz `nvidia-smi` (sledovaný průběžně `nvidia-smi dmon`). Nízké využití karty při dlouhém běhu zpravidla znamená, že karta čeká na data — úzkým hrdlem je tedy načítání (řeší se parametrem `num_workers` u `DataLoaderu`, viz [materiál o infrastruktuře PyTorche](../04-strojove-uceni/pytorch-infrastruktura.md), kapitola 1.2), nikoli výpočet.
- **`torch.profiler`** rozliší čas strávený na procesoru a na kartě a přiřadí jej k jednotlivým operacím.

> **Upozornění (synchronizační body):** Volání jako `.item()`, `.cpu()` nebo `print(tenzor)` uvnitř tréninkové smyčky vynutí **synchronizaci** procesoru a grafické karty — procesor musí počkat na dokončení výpočtu na kartě. Ve smyčce přes mnoho dávek to výrazně zpomaluje. Takové převody se provádějí mimo smyčku, nebo co nejméně často.

---

# Část B — Tipy a triky, jak zrychlit

## 6. Žebříček podle dopadu

Postupy zrychlení se liší řádovým dopadem. Je nutné je uplatňovat **shora dolů** — od největšího dopadu k nejmenšímu — a mezi jednotlivými kroky měřit:

1. **Algoritmická složitost** (kapitola 7) — postup s největším dopadem; vhodná volba algoritmu a datové struktury dokáže zkrátit dobu běhu o několik řádů.
2. **Vyhnutí se opakované práci, vektorizace, matematická reformulace a uspořádání paměti** (kapitoly 8–11) — řádové zrychlení numerického kódu.
3. **Vestavěné funkce a vhodné formáty** (kapitola 12) — dílčí, avšak snadné zisky.
4. **Mikrooptimalizace** — nejmenší dopad; má smysl až tehdy, je-li vše ostatní vyčerpáno.

Zásadní je nezačínat zdola: mikrooptimalizace kódu, jehož skutečným problémem je kvadratická složitost, nepřináší odpovídající užitek.

## 7. Algoritmická složitost

Složitost popisuje, **jak roste počet operací (a tím doba běhu) s velikostí vstupu** `n`. Je to nejdůležitější faktor výkonu, neboť pro velká `n` převáží nad vším ostatním.

### Zápis velkého O

Složitost se zapisuje notací **velké O**, která vyjadřuje horní mez růstu v závislosti na `n`, a to bez ohledu na konstanty. Zápis `O(n)` znamená, že počet operací roste úměrně velikosti vstupu; `O(n^2)`, že roste s druhou mocninou. Konstantní násobky se zanedbávají, neboť pro dostatečně velké `n` rozhoduje tvar růstu, nikoli konstanta.

Nejčastější třídy složitosti, od nejrychlejší po nejpomalejší:

| Zápis | Název | Příklad |
|---|---|---|
| `O(1)` | konstantní | přístup k prvku pole podle indexu; vyhledání v `set` nebo `dict` |
| `O(log n)` | logaritmická | binární vyhledávání v seřazeném poli |
| `O(n)` | lineární | jeden průchod seznamem |
| `O(n log n)` | kvazilineární | efektivní řazení (`sorted`) |
| `O(n^2)` | kvadratická | dvě vnořené smyčky přes tatáž data |
| `O(2^n)` | exponenciální | výčet všech podmnožin |
| `O(n!)` | faktoriálová | výčet všech permutací (pořadí) |

Rozdíl mezi třídami je pro velká `n` zásadní. Následující příklad vykreslí jejich růst ve dvou panelech a je možné jej spustit v notebooku:

```python
import numpy as np
import matplotlib.pyplot as plt

tridy = {
    "O(1)":       lambda n: np.ones_like(n),
    "O(log n)":   lambda n: np.log2(n),
    "O(n)":       lambda n: n,
    "O(n log n)": lambda n: n * np.log2(n),
    "O(n^2)":     lambda n: n ** 2,
    "O(2^n)":     lambda n: 2.0 ** n,
}

fig, (vlevo, vpravo) = plt.subplots(1, 2, figsize=(12, 4.5))

n_male = np.linspace(1, 6, 500)            # malé vstupy, lineární osa
for nazev, f in tridy.items():
    vlevo.plot(n_male, f(n_male), label=nazev)
vlevo.set_title("Malé vstupy: křivky se kříží")
vlevo.set_xlabel("velikost vstupu n")
vlevo.set_ylabel("počet operací")
vlevo.grid()
vlevo.legend()

n_velke = np.linspace(2, 40, 500)          # větší vstupy, logaritmická osa y
for nazev, f in tridy.items():
    vpravo.plot(n_velke, f(n_velke), label=nazev)
vpravo.set_yscale("log")
vpravo.set_title("Větší vstupy (log. osa y): pořadí tříd je zřejmé")
vpravo.set_xlabel("velikost vstupu n")
vpravo.set_ylabel("počet operací (log)")
vpravo.grid(which="both", alpha=0.4)
vpravo.legend()

plt.tight_layout()
plt.show()
```

Levý panel zobrazuje malé vstupy na lineární ose. Křivky se zde kříží: například pro `n = 3` vychází `n^2 = 9`, kdežto `2^n = 8`, takže exponenciální třída leží v tomto úseku pod kvadratickou. Zápis velkého O totiž popisuje chování pro **velká** `n`; u malých vstupů rozhodují konstanty a členy nižšího řádu.

Pravý panel zobrazuje větší vstupy na logaritmické ose y, na níž je pořadí tříd jednoznačné: pro `n = 40` dosahuje `2^n` řádově $10^{12}$ operací, kdežto `n^2` pouze 1600. Exponenciální růst se na logaritmické ose zobrazuje jako přímka. Pravý panel začíná hodnotou `n = 2`, neboť $\log_2 1 = 0$ a nulu nelze na logaritmické ose zobrazit.

### Třídy P a NP

Složitost se netýká jen jednotlivých algoritmů, nýbrž i **obtížnosti problémů** jako takových. Podle ní se problémy třídí:

- **Třída P** (polynomiální) zahrnuje problémy, které lze vyřešit v polynomiálním čase — tedy se složitostí `O(n^k)` pro nějaké `k` (například `O(n)`, `O(n^2)`, `O(n^3)`). Tyto problémy se považují za **prakticky řešitelné**.
- **Třída NP** zahrnuje problémy, u nichž lze navržené řešení v polynomiálním čase alespoň **ověřit**, i když jeho nalezení může být obtížné. (Zkratka NP znamená „nedeterministicky polynomiální", nikoli „nepolynomiální".) Každý problém z P je i v NP.
- **NP-úplné problémy** jsou nejobtížnější problémy v NP; patří mezi ně problém obchodního cestujícího (nalezení nejkratší trasy přes dané body), splnitelnost logické formule (SAT) či barvení grafu. Není znám žádný algoritmus, který by kterýkoli z nich řešil v polynomiálním čase.
- **NP-těžké problémy** jsou přinejmenším stejně obtížné jako NP-úplné.

Zda lze všechny problémy z NP řešit v polynomiálním čase — tedy zda platí **P = NP** — je dosud nevyřešená otázka a jeden z nejznámějších otevřených problémů informatiky.

> **Praktický důsledek:** Pro NP-těžké problémy není znám algoritmus, který by byl efektivní pro všechny vstupy. Pro velká `n` je proto přesné řešení nedosažitelné a namísto něj se používají **heuristiky a aproximace** — postupy, které nenajdou zaručeně nejlepší řešení, avšak dostatečně dobré v přijatelném čase. Narazí-li tedy úloha na NP-těžký problém, cílem není nalézt dokonalý algoritmus (ten není znám), nýbrž zvolit vhodnou aproximaci.

### Praktické využití: volba datové struktury

Nejčastějším uplatněním teorie složitosti v běžném kódu je **volba datové struktury**. Ověření, zda prvek náleží do seznamu (`x in list`), má složitost `O(n)` — prochází se celý seznam. Totéž ověření nad množinou (`x in set`) má složitost `O(1)`. Rozdíl je pro velká data zásadní; následující příklad jej změří:

```python
import timeit

setup_list = "data = list(range(100_000)); hledane = range(0, 100_000, 7)"
setup_set  = "data = set(range(100_000));  hledane = range(0, 100_000, 7)"

t_list = timeit.timeit("[x in data for x in hledane]", setup=setup_list, number=1)
t_set  = timeit.timeit("[x in data for x in hledane]", setup=setup_set,  number=1)

print(f"x in list: {t_list:.4f} s")
print(f"x in set:  {t_set:.4f} s")
```

Rozdíl bývá tisícinásobný, aniž by se změnila jediná operace — změnil se pouze typ, v němž jsou data uložena. Obdobně platí:

- **vyhledávání a jedinečnost** → `set` nebo `dict` (`O(1)`) namísto `list` (`O(n)`),
- **počítání výskytů** → `collections.Counter` namísto ručního cyklu,
- **opakované řazení** → seřadit jednou (`sorted`, `O(n log n)`) a dále využívat seřazené pořadí.

> **Upozornění:** Dvě vnořené smyčky přes tatáž data (složitost `O(n^2)`) jsou nejčastější příčinou náhlého zpomalení při růstu dat. Lze je často nahradit jedním průchodem s pomocnou množinou nebo slovníkem (`O(n)`).

## 8. Vyhnout se opakované práci

Druhým postupem s velkým dopadem je neprovádět tentýž výpočet vícekrát.

**Zapamatování výsledků (memoizace).** Vrací-li funkce pro tytéž argumenty tentýž výsledek, lze jej uložit a při opakovaném volání vrátit bez přepočítání. Slouží k tomu dekorátor `functools.cache`:

```python
from functools import cache

@cache
def fibonacci(n):
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(35))   # bez @cache by trvalo znatelně déle
```

Bez zapamatování má tento rekurzivní výpočet exponenciální složitost (tentýž mezivýsledek se počítá mnohokrát); s `@cache` se každá hodnota vyčíslí jen jednou.

**Výpočet mimo smyčku.** Hodnota, která se ve smyčce nemění, se má vyčíslit jednou před ní, nikoli opakovaně uvnitř:

```python
# nevhodně: len(data) se volá v každém kroku
for i in range(len(data)):
    ...

# vhodně: vyčísleno jednou
n = len(data)
for i in range(n):
    ...
```

**Vektorizace.** Nejvýznamnějším případem vyhnutí se opakované práci v numerickém kódu je nahrazení smyčky v Pythonu operací nad celým polem; věnuje se jí následující kapitola.

## 9. Vektorizace

**Vektorizace** je nahrazení smyčky v jazyce Python, která zpracovává data po jednotlivých prvcích, jedinou operací nad celým polem. Knihovny NumPy a PyTorch takovou operaci provedou uvnitř přeloženého kódu (v jazyce C, případně na grafické kartě) nad souvisle uloženými daty jednoho typu. V numerickém kódu jde po volbě algoritmu o postup s největším praktickým dopadem.

### 9.1 Proč je smyčka v Pythonu pomalá

Při každém průchodu smyčkou interpret zjišťuje typ hodnoty, vyhledává odpovídající operaci a vytváří nový objekt pro výsledek. U milionu prvků se tato režie opakuje milionkrát. Vektorizovaná operace tuto režii vynaloží jednou a samotný výpočet proběhne v přeloženém cyklu, který navíc využívá vektorové instrukce procesoru (SIMD) zpracovávající několik čísel současně.

```python
import numpy as np, time

x = np.random.rand(1_000_000)

t = time.perf_counter()
s = 0.0
for hodnota in x:                  # smyčka po jednotlivých prvcích
    s += hodnota * hodnota
t_cyklus = time.perf_counter() - t

t = time.perf_counter()
s_vektor = np.sum(x * x)           # jediná operace nad celým polem
t_vektor = time.perf_counter() - t

print(f"smyčka:      {t_cyklus:.3f} s")
print(f"vektorizace: {t_vektor:.4f} s")
print(np.isclose(s, s_vektor))     # True — výsledek je shodný
```

Vektorizovaná varianta bývá o jeden až dva řády rychlejší; přesný poměr závisí na stroji.

### 9.2 Podmínky a logické masky

Podmínka uvnitř smyčky (`if`) se nahrazuje funkcí `np.where`, výběr prvků splňujících podmínku **logickou maskou** — polem hodnot `True`/`False` téhož tvaru:

```python
import numpy as np

signal = np.array([0.5, -1.2, 3.4, -0.1, 2.2])

orezany = np.where(signal < 0, 0.0, signal)   # záporné hodnoty nahradit nulou
print(orezany)                                # [0.5 0.  3.4 0.  2.2]

maska = signal > 1.0                          # logická maska
print(signal[maska])                          # [3.4 2.2]
print(maska.sum())                            # 2 — počet hodnot nad prahem
```

### 9.3 Broadcasting

Operace mezi poli **různého tvaru** umožňuje mechanismus **broadcasting**. Tvary obou polí se porovnávají od posledního rozměru; dva rozměry jsou slučitelné, jsou-li shodné, nebo je-li jeden z nich roven 1, a chybějící rozměr se považuje za 1. Rozměr velikosti 1 se pro výpočet rozšíří na velikost druhého pole, aniž by se data fyzicky kopírovala.

Typickým příkladem je standardizace sloupců matice, tedy odečtení průměru a vydělení směrodatnou odchylkou každého sloupce:

```python
import numpy as np

X = np.array([[1.0, 200.0],
              [2.0, 300.0],
              [3.0, 400.0]])               # tvar (3, 2)

prumer = X.mean(axis=0)                    # tvar (2,), rozšíří se na (3, 2)
odchylka = X.std(axis=0)                   # tvar (2,)
X_std = (X - prumer) / odchylka

print(np.round(X_std, 4))
# [[-1.2247 -1.2247]
#  [ 0.      0.    ]
#  [ 1.2247  1.2247]]
```

Broadcasting dovoluje vektorizovat i výpočty, které by jinak vyžadovaly vnořené smyčky. Následující příklad vypočte matici vzdáleností mezi `n` body a `k` středy (výpočet, na němž stojí například shlukovací algoritmy), nejprve dvěma smyčkami, poté jedinou operací:

```python
import numpy as np, time

rng = np.random.default_rng(0)
body = rng.random((5000, 3))               # n = 5000 bodů, d = 3 příznaky
centra = rng.random((8, 3))                # k = 8 středů

t = time.perf_counter()
D_cyklus = np.empty((len(body), len(centra)))
for i, b in enumerate(body):
    for j, c in enumerate(centra):
        D_cyklus[i, j] = np.sqrt(np.sum((b - c) ** 2))
t_cyklus = time.perf_counter() - t

t = time.perf_counter()
rozdily = body[:, None, :] - centra[None, :, :]   # (n, 1, d) - (1, k, d) -> (n, k, d)
D_vektor = np.sqrt((rozdily ** 2).sum(axis=2))    # součet přes d -> (n, k)
t_vektor = time.perf_counter() - t

print(f"smyčky:       {t_cyklus:.3f} s")
print(f"broadcasting: {t_vektor:.4f} s")
print(np.allclose(D_cyklus, D_vektor))           # True
```

Zápis `None` v indexu vkládá nový rozměr velikosti 1; díky němu se každý bod porovná s každým středem.

### 9.4 Nástrahy vektorizace

> **Upozornění (`np.vectorize` není vektorizace):** Funkce `np.vectorize` navzdory svému názvu kód nevektorizuje. Jde o pohodlný obal, který uvnitř provádí tutéž smyčku v Pythonu, a nepřináší proto zrychlení:
> ```python
> import numpy as np, timeit
>
> x = np.random.rand(1_000_000)
> f = np.vectorize(lambda v: v * v)
>
> print(timeit.timeit(lambda: f(x),  number=3))   # řádově desetiny sekundy
> print(timeit.timeit(lambda: x * x, number=3))   # řádově tisíciny sekundy
> ```

**Paměťová náročnost mezivýsledků.** Broadcasting může vytvořit velmi rozměrné mezivýsledky. Pole `rozdily` z předchozího příkladu má tvar `(n, k, d)`; pro `n = 100 000`, `k = 1 000` a `d = 128` v typu `float64` by zabíralo přibližně 102 GB. Řešením je zpracování po dávkách, nebo matematická reformulace (kapitola 10). Druhou mocninu vzdálenosti lze rozepsat jako

$$\lVert a - b \rVert^2 = \lVert a \rVert^2 + \lVert b \rVert^2 - 2\, a \cdot b ,$$

čímž se výpočet převede na násobení matic bez trojrozměrného mezivýsledku:

```python
D2 = (body ** 2).sum(axis=1)[:, None] + (centra ** 2).sum(axis=1)[None, :] - 2 * body @ centra.T
D = np.sqrt(np.maximum(D2, 0))     # zaokrouhlovací chyby mohou dát nepatrně záporné hodnoty
print(np.allclose(D, D_vektor))    # True
```

**Sekvenční závislost.** Vektorizovat nelze přímo výpočet, v němž každý krok závisí na výsledku předchozího. Příkladem je exponenciální vyhlazování signálu $y_t = \alpha\, x_t + (1 - \alpha)\, y_{t-1}$. Pro řadu takových výpočtů však existují hotové vektorizované funkce — pro rekurentní filtry `scipy.signal.lfilter`, pro kumulativní součty `np.cumsum`:

```python
import numpy as np
from scipy.signal import lfilter

alfa = 0.1
x = np.random.default_rng(0).random(10_000)

y = np.empty_like(x)                       # smyčka: každý krok závisí na předchozím
predchozi = 0.0
for t, hodnota in enumerate(x):
    predchozi = alfa * hodnota + (1 - alfa) * predchozi
    y[t] = predchozi

y_filtr = lfilter([alfa], [1, -(1 - alfa)], x)   # tentýž rekurentní filtr
print(np.allclose(y, y_filtr))                   # True
```

Neexistuje-li vektorizovaný ekvivalent, lze smyčku přeložit do strojového kódu nástrojem Numba (kapitola 14).

**Čitelnost.** Vektorizovaný zápis bývá hutný. U netriviálních operací je vhodné komentářem uvést tvary polí, jak ukazují příklady výše.

**PyTorch.** Totéž platí pro tenzory v knihovně PyTorch. Na grafické kartě je smyčka v Pythonu nad jednotlivými prvky tenzoru obzvláště nevhodná, neboť každá dílčí operace navíc vyžaduje samostatné spuštění výpočtu na kartě.

## 10. Matematická reformulace

Někdy lze výpočet zrychlit nebo stabilizovat tím, že se **přepíše do matematicky rovnocenné, avšak výhodnější podoby**.

**Součet logaritmů místo součinu.** Násobí-li se mnoho malých čísel (typicky pravděpodobností), výsledek rychle **podteče** pod nejmenší zobrazitelné číslo a stane se nulou. Protože logaritmus převádí součin na součet (`log(a·b) = log a + log b`), lze namísto součinu hodnot sečíst jejich logaritmy — výsledek je stabilní a výpočet se součty bývá i rychlejší:

```python
import numpy as np

p = np.full(1000, 0.001)       # tisíc malých pravděpodobností

print(np.prod(p))              # 0.0 — součin podtekl na nulu
print(np.sum(np.log(p)))       # -6907.76 — součet logaritmů, stabilní
```

**Log-sum-exp.** Příbuzným postupem se stabilizuje výpočet funkce softmax: před umocněním se od hodnot odečte jejich maximum, čímž se zabrání **přetečení** funkce `exp` u velkých hodnot, aniž by se změnil výsledek:

```python
import numpy as np

x = np.array([1000.0, 1001.0, 1002.0])

# naivní výpočet: np.exp(x) přeteče na nekonečno
m = x.max()
softmax = np.exp(x - m) / np.exp(x - m).sum()
print(softmax)                 # [0.09003, 0.24473, 0.66524]
```

Obě úpravy se týkají i numerické stability výpočtu: nejde pouze o rychlost, nýbrž především o správnost výsledku při mezních hodnotách.

## 11. Uspořádání paměti a cache

Rychlost přístupu k datům závisí na tom, jak jsou uložena v paměti. Procesor načítá paměť po souvislých blocích (tzv. cache lines); čtení **souvislých** dat je proto podstatně rychlejší než čtení dat roztroušených.

**Řádkové versus sloupcové uložení.** Vícerozměrné pole je v paměti uloženo jako jediná souvislá posloupnost čísel, kterou lze uspořádat dvěma způsoby: po řádcích (**C-order**, výchozí v NumPy), nebo po sloupcích (**Fortran-order**). Uložení popisují **kroky** (strides) — počet bajtů, o který je nutné se v paměti posunout k dalšímu prvku v daném rozměru:

```python
import numpy as np

A = np.zeros((3, 4))                    # float64, tj. 8 bajtů na prvek
print(A.strides)                        # (32, 8): další řádek o 32 B, další sloupec o 8 B
print(A.T.strides)                      # (8, 32): transpozice pouze prohodí kroky
print(A.flags["C_CONTIGUOUS"])          # True
print(A.T.flags["C_CONTIGUOUS"])        # False
```

Transpozice tedy data nekopíruje; pouze prohodí kroky, takže výsledné pole již není řádkově souvislé.

Rychlejší je čtení **podél té osy, která je v paměti souvislá**. Rozdíl se však neprojeví u každé operace: funkce NumPy jako `sum` pořadí průchodu samy přizpůsobují uložení pole. Zřetelně se projeví tam, kde operace musí číst data v nesouvislém pořadí — například při kombinaci pole s jeho transpozicí:

```python
import numpy as np, timeit

A = np.random.rand(4000, 4000)

stejne_ulozeni  = timeit.timeit(lambda: A + A,   number=10)   # obě pole se čtou souvisle
smisene_ulozeni = timeit.timeit(lambda: A + A.T, number=10)   # A.T se čte nesouvisle

print(f"A + A:   {stejne_ulozeni:.3f} s")
print(f"A + A.T: {smisene_ulozeni:.3f} s")
```

Druhá operace bývá přibližně dvakrát pomalejší, přestože počet sčítání je shodný; přesný poměr závisí na stroji. Bude-li se s nesouvislým polem pracovat opakovaně, je vhodné vytvořit jeho souvislou kopii funkcí `np.ascontiguousarray`.

> **Přesah (PyTorch):** Metoda `.view()` tenzoru vyžaduje souvislé uložení. Po transpozici či jiné operaci, která pouze prohodí kroky, skončí chybou. Řešením je volání `.contiguous()`, které vytvoří souvislou kopii, případně metoda `.reshape()`, jež kopii vytvoří sama, je-li to nutné.

**Datové typy.** Volba typu ovlivňuje paměť i rychlost. Pole typu `float32` zabírá poloviční paměť oproti `float64` a na grafické kartě se zpracovává rychleji; pro mnoho úloh strojového učení je přesnost `float32` dostačující (k využití nižší přesnosti při tréninku viz [materiál o infrastruktuře PyTorche](../04-strojove-uceni/pytorch-infrastruktura.md), kapitola 3.5):

```python
import numpy as np

velke = np.ones((10_000, 10_000), dtype=np.float64)   # ~800 MB
male  = np.ones((10_000, 10_000), dtype=np.float32)   # ~400 MB
print(velke.nbytes / 1e6, "MB")
print(male.nbytes / 1e6, "MB")
```

**Pohledy versus kopie.** Řez pole (například `a[2:5]`) vrací **pohled** — nový objekt nad týmiž daty, bez kopírování. Pohled je proto levný, avšak změna provedená jeho prostřednictvím se projeví i v původním poli. Indexování seznamem indexů či logickou maskou naopak vytváří **kopii**, stejně jako aritmetické operace, které ukládají výsledek do nového pole:

```python
import numpy as np

a = np.arange(10)
pohled = a[2:5]                         # řez vrací pohled
pohled[0] = 99
print(a[2])                             # 99 — změna se projevila v původním poli

kopie = a[[2, 3, 4]]                    # indexování seznamem vrací kopii
print(np.shares_memory(a, pohled))      # True
print(np.shares_memory(a, kopie))       # False
```

U velkých polí zbytečné kopie prodlužují výpočet i spotřebovávají paměť. Opakované úpravy téhož pole lze provádět na místě, bez vytváření nového pole — operátory `+=`, `*=` nebo parametrem `out=` funkcí NumPy.

## 12. Vestavěné funkce a vhodné formáty

**Vestavěné funkce a komprehenze.** Vestavěné funkce (`sum`, `min`, `max`, `any`, `all`) a komprehenze seznamů jsou implementovány v jazyce C a jsou rychlejší než rovnocenná smyčka v Pythonu:

```python
import timeit

cyklus = timeit.timeit(
    "s = 0\nfor i in range(10000):\n    s += i * i", number=1000
)
vestavene = timeit.timeit(
    "sum(i * i for i in range(10000))", number=1000
)
print(f"ruční cyklus:      {cyklus:.3f} s")
print(f"vestavěná funkce:  {vestavene:.3f} s")
```

**Spojování řetězců.** Řetězce se spojují metodou `"".join(seznam)`, nikoli opakovaným `+=` ve smyčce; opakované spojování totiž pokaždé vytváří nový řetězec (viz příklad v kapitole 3).

**Vhodné formáty dat.** Opakované načítání velkých dat z textového formátu (CSV) je pomalé, neboť vyžaduje převod textu na čísla. Pro mezivýsledky jsou vhodnější **binární formáty** — `.npy` (NumPy) či `parquet` (tabulková data) —, které se načítají řádově rychleji a zabírají méně místa.

## 13. Kdy přestat

Optimalizace má svou míru. Platí několik zásad, kdy ustat:

- **Dostačující rychlost.** Je-li program dostatečně rychlý pro svůj účel, další optimalizace nepřináší hodnotu.
- **Nepatrný dopad.** Zrychlení místa, které zabírá zlomek celkového času (Amdahlův zákon, kapitola 2), nepřináší odpovídající užitek.
- **Cena za čitelnost.** Překročí-li optimalizace únosnou mez zhoršení čitelnosti, je nutné zvážit, zda zisk vyváží pozdější obtížnější údržbu. Optimalizovaný úsek je vhodné opatřit komentářem vysvětlujícím, proč je napsán neobvykle.
- **Zachování správnosti.** Žádné zrychlení není přijatelné za cenu nesprávného výsledku; po každé úpravě je nutné ověřit, že výstup zůstal nezměněný (viz [materiál o testování](testovani.md)).

## 14. Jít ještě dál: paralelizace a kompilace

Vyčerpá-li se potenciál jednovláknové optimalizace, lze pokračovat dvěma směry, které tento materiál pouze naznačuje:

- **Paralelní zpracování** rozdělí práci mezi více jader procesoru (modul `multiprocessing`) či strojů. V jazyce Python je přitom třeba počítat s tzv. **globálním zámkem interpretu (GIL)**, který omezuje souběžné provádění vláken, takže pro výpočetně náročné úlohy se používají samostatné procesy, nikoli vlákna.
- **Kompilace kritického kódu** převede nejnáročnější úsek do strojového kódu. Nástroje `Numba` (překlad vybraných funkcí za běhu) a `Cython` (překlad do jazyka C) dokáží zrychlit numerické smyčky, které nelze vektorizovat, o jeden až dva řády.

Oba směry jsou samostatná témata přesahující rozsah tohoto materiálu; uvádějí se jako naznačení, kam vede další postup.

## 15. Shrnutí

Výkon se nejprve **měří**, teprve poté optimalizuje — a to pouze na místě, které měření označí za úzké hrdlo (Amdahlův zákon). K měření slouží `timeit` (úseky), `cProfile` a `line_profiler` (funkce a řádky), `tracemalloc` (paměť) a vzorkovací profilery `py-spy` a `scalene` (běžící a vzdálené procesy); v kontextu strojového učení se rozlišuje úzké hrdlo v načítání dat od výpočtu na grafické kartě. Postupy zrychlení se uplatňují shora dolů podle dopadu: nejprve **algoritmická složitost** a volba datové struktury (`set`/`dict` namísto `list`), poté **vektorizace** (operace nad celým polem, logické masky, broadcasting; `np.vectorize` vektorizací není), **matematická reformulace** (součet logaritmů, log-sum-exp) a **uspořádání paměti** (řádkové versus sloupcové, souvislost, `float32`, pohledy a kopie), nakonec vestavěné funkce a vhodné formáty. Optimalizace se zastaví, jakmile je rychlost dostačující nebo by další zisk nevyvážil ztrátu čitelnosti; výsledek musí po každé úpravě zůstat nezměněný. Dalším směrem je paralelizace a kompilace kritického kódu.

> **Další čtení:** dokumentace modulů [`timeit`](https://docs.python.org/3/library/timeit.html), [`cProfile`](https://docs.python.org/3/library/profile.html) a [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html); dokumentace [NumPy](https://numpy.org/doc/stable/) ke vnitřnímu uspořádání polí; vzorkovací profilery [py-spy](https://github.com/benfred/py-spy) a [Scalene](https://github.com/plasma-umass/scalene).
