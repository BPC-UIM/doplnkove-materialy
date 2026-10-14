# Kontrolní seznam pro psaní funkcí

*Výukový materiál — zásady pro psaní funkcí v jazyce Python*

Tento kontrolní seznam shrnuje zásady, podle nichž lze posoudit kvalitu jednotlivé funkce. Vychází z doporučení [PEP 8](https://peps.python.org/pep-0008/) (styl kódu) a [PEP 257](https://peps.python.org/pep-0257/) (docstringy). Jednotlivé body slouží ke kontrole při psaní nové funkce i při revizi hotového kódu.

## 1. Název

- Název funkce je srozumitelný a popisný; vyjadřuje, co funkce dělá, nikoli jak.
- Název je zapsán ve tvaru `snake_case` (například `get_user_data`).
- Název neobsahuje zkratky, nejsou-li obecně známé.

## 2. Signatura

- Všechny parametry i návratová hodnota mají typové anotace (viz [materiál o typování](typovani-promennych.md)).
- Parametry mají výchozí hodnoty tam, kde to odpovídá jejich povaze.
- Výchozí hodnotou není měnitelný objekt (`list = []`, `dict = {}`), neboť výchozí objekt vzniká jen jednou a je sdílen mezi všemi voláními funkce; namísto něj se použije `None` a objekt se vytvoří uvnitř funkce.
- Krátká signatura se zapisuje na jeden řádek:

  ```python
  def fce(a: int, b: int) -> int:
      ...
  ```

- Dlouhá signatura se rozdělí na více řádků, každý parametr na samostatný řádek. Uzavírací závorka s návratovým typem se umístí na začátek samostatného řádku:

  ```python
  def fce(
      a: int,
      b: int,
      c: int,
      d: str = "default",
  ) -> int:
      ...
  ```

- Oba způsoby zápisu se v jedné signatuře nekombinují (tj. část parametrů na jednom řádku a zbytek pod sebou).

> **Poznámka (umístění uzavírací závorky):** PEP 8 připouští odsazení uzavírací závorky na úroveň parametrů i její umístění na začátek řádku. Při odsazení na úroveň parametrů však parametry vizuálně splývají s tělem funkce, které je odsazeno stejně. Umístění na začátek řádku obě části zřetelně odděluje; tento tvar vytvářejí i nástroje pro automatické formátování kódu (`black`, `ruff format`).

## 3. Dokumentace

- Funkce má docstring podle PEP 257.
- Docstring obsahuje:
  - účel funkce (co dělá a proč existuje),
  - popis parametrů (typ a význam),
  - popis návratové hodnoty (typ a význam),
  - výjimky, které funkce vyvolává, pokud nějaké vyvolává.
- Styl docstringů je v celém projektu jednotný (například NumPy nebo Google); příklad v kapitole 8 používá styl NumPy.

## 4. Validace vstupů

- Je-li to podstatné, funkce ověřuje typ a rozsah vstupních hodnot.
- Při neplatném vstupu funkce vyvolá výstižnou výjimku: `TypeError` při nesprávném typu, `ValueError` při nepřípustné hodnotě správného typu.
- Validace se provádí především na rozhraní, tj. ve funkcích volaných zvenčí, nikoli v každé interní pomocné funkci.

> **Upozornění (`bool` je podtřídou `int`):** Logické hodnoty `True` a `False` jsou v jazyce Python instancemi typu `int`:
> ```python
> print(isinstance(True, int))   # True
> print(True + True)             # 2
> ```
> Kontrola `isinstance(x, int)` proto propustí i logické hodnoty. Má-li být logická hodnota odmítnuta, je nutné ji vyloučit výslovně, jak ukazuje příklad v kapitole 8.

## 5. Návratová hodnota

- Funkce vrací jednoznačně definovanou hodnotu, případně `None`, odpovídá-li to jejímu účelu.
- Funkce nevrací tzv. magické hodnoty (například `-1` či `""`) jako náhradu výjimky.
- Vrací-li funkce více hodnot, použije se namísto prosté n-tice `NamedTuple` nebo `dataclass` (viz [materiál o základech objektově orientovaného programování](zaklady-oop.md), kapitola 9), aby byl zřejmý význam jednotlivých hodnot.

## 6. Struktura

- Funkce má jedinou odpovědnost (princip jediné odpovědnosti, *Single Responsibility Principle*).
- Funkce je krátká a přehledná, orientačně do přibližně 20 řádků.
- Delší funkce se rozdělí na několik menších pomocných funkcí.

## 7. Testovatelnost

- Funkce je deterministická: pro stejné vstupy vrací stejné výstupy.
- Funkci lze snadno otestovat, přinejmenším pro běžný průběh (tzv. šťastnou cestu) a pro hraniční případy (viz [materiál o testování](../02-overovani-a-ladeni/testovani.md)).
- Má-li funkce vedlejší účinky (vstup a výstup, náhodnost, závislost na čase), je navržena tak, aby je bylo možné při testování řídit — například předáním zárodku generátoru náhody (viz [materiál o reprodukovatelnosti](../03-projekt-a-prostredi/reprodukovatelnost-seedy.md), kapitola 5) nebo nahrazením závislosti testovacím dvojníkem (viz [materiál o testování](../02-overovani-a-ladeni/testovani.md), kapitola 7).

## 8. Příklad

Následující funkce splňuje body kontrolního seznamu:

```python
def my_function(
    a: int,
    b: int = 10,
) -> int:
    """
    Spočítá součet dvou celých čísel.

    Parameters
    ----------
    a : int
        Povinný vstup - první celé číslo.
    b : int, optional
        Nepovinný vstup - druhé celé číslo.
        Výchozí hodnota je 10.

    Returns
    -------
    int
        Součet čísel `a` a `b`.

    Raises
    ------
    TypeError
        Pokud `a` nebo `b` nejsou celá čísla
        (hodnoty typu `bool` se za celá čísla nepovažují).
    """
    # Validace vstupů; bool je podtřídou int, proto se vylučuje výslovně
    for hodnota in (a, b):
        if isinstance(hodnota, bool) or not isinstance(hodnota, int):
            raise TypeError("Parametry a a b musí být celá čísla.")

    # Výpočet
    result = a + b

    return result
```

Ověření chování funkce:

```python
print(my_function(2, 3))       # 5
print(my_function(2))          # 12

try:
    my_function(True, 3)
except TypeError as chyba:
    print(chyba)               # Parametry a a b musí být celá čísla.
```

## 9. Shrnutí

Kvalitně napsaná funkce má srozumitelný název ve tvaru `snake_case` a přehledně zapsanou signaturu s typovými anotacemi a bez měnitelných výchozích hodnot. Její docstring popisuje účel, parametry, návratovou hodnotu a výjimky. Vstupy ověřuje především na rozhraní, přičemž při kontrole celých čísel výslovně vylučuje logické hodnoty. Vrací jednoznačně definovanou hodnotu bez magických hodnot, plní jedinou odpovědnost a lze ji spolehlivě otestovat.

> **Další čtení:** [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/); [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/).
