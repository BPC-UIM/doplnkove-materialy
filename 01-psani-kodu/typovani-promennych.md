# Typové anotace proměnných v jazyce Python

*Výukový materiál — typové anotace (type hints)*

## 1. Účel a přínosy typových anotací

Python je dynamicky typovaný jazyk: typ proměnné se určuje až za běhu programu a zpravidla se nikam neuvádí. Typové anotace na této skutečnosti nic nemění — jedná se o **nepovinné poznámky o typu**, jejichž přínos spočívá v následujícím:

- **dokumentační funkce** — typ je uveden přímo v hlavičce funkce, takže je z ní zřejmé, jaké hodnoty funkce přijímá a jaké vrací,
- **podpora ve vývojovém prostředí** — editor nabízí doplňování a upozorňuje na chyby ještě před spuštěním programu,
- **statická analýza** — nástroje jako `mypy` či `pyright` odhalí část chyb bez nutnosti program spouštět,
- **snazší údržba kódu** — při změně typu na jednom místě nástroj označí všechna místa, která přestala odpovídat.

> **Upozornění:** Typové anotace nejsou za běhu vynucovány. Následující kód proběhne bez chyby a vypíše `ahojahoj`:
> ```python
> def zdvoj(x: int) -> int:
>     return x * 2
> print(zdvoj("ahoj"))   # interpret typ nekontroluje
> ```
> Kontrolu typů provádí teprve samostatný nástroj statické analýzy, jehož použití je popsáno v kapitole 5.

## 2. Syntaxe zápisu

**Proměnná:**
```python
jmeno: str = "Eva"
vek: int          # samotná anotace bez přiřazení proměnnou nevytváří
```

**Funkce** (typ argumentu se uvádí za dvojtečkou, návratový typ za znakem `->`):
```python
def pozdrav(jmeno: str, hlasite: bool = False) -> str:
    ...
```

**Kolekce** — od verze Pythonu 3.9 se používají přímo vestavěné typy:
```python
cisla: list[int]
mapa: dict[str, float]
dvojice: tuple[int, str]
mnozina: set[str]
```

## 3. Varianty zápisu

| Požadavek | Moderní zápis (3.10+) | Starší zápis (`typing`) |
|---|---|---|
| Hodnota, nebo `None` | `int \| None` | `Optional[int]` |
| Více přípustných typů | `int \| str` | `Union[int, str]` |
| Seznam celých čísel | `list[int]` | `List[int]` |
| Libovolný typ (vypíná kontrolu) | `Any` | `Any` |
| Funkce jako argument | `Callable[[int], str]` | totéž z `typing` |
| Výčet konkrétních hodnot | `Literal["r", "w"]` | totéž z `typing` |

> **Upozornění k verzím Pythonu:** Zápis `int | None` a `list[int]` je dostupný až od novějších verzí jazyka. Ve starším kódu i v dokumentaci se vyskytují tvary `Optional`, `Union` a `List` importované z modulu `typing`; jde o významově shodné zápisy. V rámci jednoho projektu se doporučuje obě varianty nekombinovat.

## 4. Časté chyby a nástrahy

1. **Měnitelný výchozí argument.** Místo zápisu `def f(x: list = [])` se parametr anotuje jako `def f(x: list | None = None)` a seznam se vytvoří uvnitř těla funkce; důvod uvádí [materiál o psaní funkcí](jak-psat-funkce.md), kapitola 2.
2. **Odkaz na dosud nedefinovaný typ** (například třída odkazující sama na sebe). Řešením je buď zápis názvu typu v uvozovkách (`-> "MojeTrida"`), nebo uvedení řádku `from __future__ import annotations` na začátku souboru.
3. **Nadměrné anotování.** Cílem je čitelnost, nikoli formální úplnost. U zřejmých případů (`i = 0`) anotace nepřináší užitek; vhodné je typovat především **rozhraní**, tj. hlavičky funkcí, veřejné API a návratové hodnoty.

## 5. Spuštění statické kontroly

Anotace samy o sobě chyby neodhalí; k tomu slouží nástroj statické analýzy. Nejrozšířenější jsou `mypy` a `pyright`. Instalace se provádí pomocí správce balíčků `pip`:

```bash
pip install mypy        # případně: pip install pyright
```

Uvažujme soubor `priklad.py` obsahující dvě záměrné typové chyby:

```python
def zdvoj(x: int) -> int:
    return x * 2

cislo: int = "deset"      # přiřazení řetězce do proměnné typu int
print(zdvoj("ahoj"))      # předání řetězce tam, kde se očekává int
```

**Kontrola nástrojem mypy** se spustí příkazem `python -m mypy priklad.py`. Výstup v konzoli:

```text
priklad.py:4: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
priklad.py:5: error: Argument 1 to "zdvoj" has incompatible type "str"; expected "int"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```

**Kontrola nástrojem pyright** se spustí příkazem `python -m pyright priklad.py`. Výstup má odlišný formát:

```text
  priklad.py:4:14 - error: Type "Literal['deset']" is not assignable to declared type "int"
    "Literal['deset']" is not assignable to "int" (reportAssignmentType)
  priklad.py:5:19 - error: Argument of type "Literal['ahoj']" cannot be assigned to parameter "x" of type "int" in function "zdvoj" (reportArgumentType)
2 errors, 0 warnings, 0 informations
```

Každé hlášení uvádí soubor, číslo řádku (u nástroje pyright i sloupce) a popis nesouladu; nástroj `mypy` doplňuje v hranatých závorkách kód chyby. Po opravě obou chyb (např. `cislo: int = 10` a `zdvoj(5)`) ohlásí nástroje bezchybný stav:

```text
mypy:    Success: no issues found in 1 source file
pyright: 0 errors, 0 warnings, 0 informations
```

> **Poznámka:** Konkrétní formulace hlášení se může mezi jednotlivými verzemi nástrojů mírně lišit; podstatná je informace o umístění a povaze chyby, nikoli doslovné znění textu.

> **Poznámka ke spouštění (zejména na systému Windows):** Nástroj se zde spouští ve tvaru `python -m mypy ...`, tedy jako modul interpretu Pythonu. Tento zápis je spolehlivější než přímý příkaz `mypy ...`, který selže s hlášením `'mypy' is not recognized` v případě, že se příslušná složka `Scripts` nenachází v systémové proměnné `PATH`. Forma `python -m <nástroj>` tuto závislost obchází a funguje obdobně i pro další nástroje (`pip`, `pytest` aj.; ke spouštění jako modul viz též [materiál o struktuře projektu](../03-projekt-a-prostredi/struktura-projektu.md), kapitola 6).

## 6. Doporučení pro praxi

Anotovat je vhodné především **hlavičky funkcí**, nikoli každou lokální proměnnou. Na projekt se doporučuje pravidelně spouštět nástroj statické analýzy. Je třeba mít na paměti, že typová anotace představuje závazek vůči čtenáři a vůči nástroji — interpret jazyka jeho dodržení nevynucuje.
