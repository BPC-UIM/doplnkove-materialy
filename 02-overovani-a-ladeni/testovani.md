# Testování kódu

*Výukový materiál — automatizované testování v jazyce Python*

Tento text je úvodním rozcestníkem do problematiky testování. Poskytuje základní orientaci a odkazy na zdroje, v nichž lze pokračovat do hloubky.

## 1. Proč testovat

**Test** je kód, který automaticky ověřuje, že se jiný kód chová podle očekávání. Testování bývá vnímáno jako práce navíc, a v krátkodobém pohledu jí skutečně je. Rozhodující je však pohled dlouhodobý: **náklad na napsání testu je jednorázový a předchází vývoji, kdežto jeho užitek je průběžný** — projeví se při každé pozdější úpravě kódu.

Přínosy testů přesahují pouhé odhalování chyb:

- **bezpečná úprava kódu** — testy umožňují měnit a vylepšovat existující kód s jistotou, že se neporušilo dosavadní chování; bez nich se úpravám funkčního kódu člověk vyhýbá ze strachu,
- **spustitelná specifikace** — test popisuje, co má kód dělat, a na rozdíl od komentáře nemůže zastarat, aniž by na to upozornil,
- **rychlejší lokalizace chyby** — selže-li konkrétní test, je zřejmé, která část kódu selhala,
- **důvěra** — sada procházejících testů dává podklad k tvrzení, že kód funguje.

Nejsilnějším argumentem není odhalení chyby v okamžiku psaní, nýbrž právě možnost později do kódu zasahovat bez obav.

## 2. Assert versus test

Základním stavebním prvkem testu je příkaz `assert`. Ten ověří podmínku; je-li nepravdivá, vyvolá výjimku `AssertionError`, případně s doplňujícím sdělením:

```python
assert x > 0
assert len(vysledek) == 3, "očekávány tři shluky"
```

Je třeba rozlišit dvojí užití. **Holý `assert` v běžném kódu** je jednorázová kontrola předpokladu, vázaná na konkrétní běh programu. **Test** je naproti tomu `assert` umístěný ve **vyhrazené funkci**, kterou spouští a vyhodnocuje testovací nástroj — systematicky, opakovatelně a nezávisle na hlavním programu.

Rozdíl tedy nespočívá v samotném příkazu `assert`, nýbrž v jeho zasazení: příležitostná kontrola za běhu oproti systematickému, opakovatelnému ověření řízenému nástrojem.

> **Další čtení:** oficiální dokumentace, [příkaz `assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement).

## 3. Druhy testů

Testy se člení podle rozsahu ověřované jednotky, od nejužšího po nejširší:

- **Jednotkový test** ověřuje nejmenší samostatnou jednotku — jednu funkci nebo jednu třídu — v izolaci od zbytku.
- **Integrační test** ověřuje součinnost více jednotek, například celý zpracovatelský řetězec (pipeline).
- **Smoke test** je rychlé ověření, že program vůbec proběhne a základní chování je v pořádku; slouží k odhalení hrubých selhání ještě před podrobnějším zkoumáním.

Užší testy jsou rychlejší a přesněji lokalizují chybu; širší testy ověřují, že jednotky fungují dohromady.

```mermaid
flowchart LR
    U["Jednotkový test<br/>jedna funkce nebo třída"]
    I["Integrační test<br/>součinnost více jednotek"]
    S["Smoke test<br/>běh celého programu"]
    U -- "širší rozsah" --> I
    I -- "širší rozsah" --> S
```

Textový popis schématu:

- Zleva doprava roste rozsah ověřované části programu: od jedné funkce či třídy přes součinnost více jednotek po běh celého programu.
- Směrem doleva roste rychlost testu a přesnost, s níž test určí místo chyby; směrem doprava roste šíře ověřeného chování.

## 4. Anatomie testu: Arrange–Act–Assert

Přehledný test se člení do tří kroků, jejichž počáteční písmena tvoří pojmenování vzoru **Arrange–Act–Assert**: připravit vstupy, provést operaci, ověřit výsledek.

```python
def test_prumer():
    data = [2, 4, 6]              # Arrange — příprava vstupů
    vysledek = prumer(data)       # Act    — provedení operace
    assert vysledek == 4          # Assert — ověření výsledku
```

Toto členění udržuje test čitelný a soustředěný na jedinou ověřovanou skutečnost.

## 5. Jak testovat jednotlivé jednotky

**Funkce** se testuje nejsnáze: pro známý vstup se ověří očekávaný výstup.

```python
def test_secti():
    assert secti(2, 3) == 5
```

**Třída** sdružuje stav a chování, proto se testuje ve dvou ohledech: vytvoří se instance, provede se operace a ověří se buď její výsledek, nebo výsledný stav objektu. Typickým příkladem je vzor `nauc`/`predikuj` (v knihovnách známý jako `fit`/`predict`):

```python
def test_model_vraci_spravny_tvar():
    model = Model()
    model.nauc(trenovaci_data)
    predikce = model.predikuj(testovaci_data)
    assert predikce.shape == (len(testovaci_data),)
```

**Řetězec (pipeline)** se ověřuje integračním testem: zkoumá se, zda posloupnost jednotek dohromady vede ke správnému výsledku. Takových testů bývá méně a jsou širší než testy jednotkové.

## 6. Vlastnosti dobrého testu

- **Ověřuje jedinou skutečnost.** Selže-li, je okamžitě zřejmé, co je vadné.
- **Je nezávislý.** Nezávisí na jiných testech ani na pořadí spuštění.
- **Je deterministický.** Při každém spuštění dává týž výsledek (viz kapitola 7).
- **Má srozumitelný název.** Název vyjadřuje, co test ověřuje.
- **Poskytuje vypovídající chybové sdělení.** Při selhání objasní příčinu.

```python
def test_popisky_jsou_v_rozsahu():
    labels = model.predikuj()
    assert labels.min() >= 0, "popisky nesmějí být záporné"
    assert labels.max() <= 2, "popisky musí být menší než počet shluků"
```

## 7. Testování obtížných případů

Některé situace vyžadují zvláštní přístup; následující patří k nejčastějším.

**Náhoda a nedeterminismus.** Obsahuje-li kód náhodu (například náhodnou inicializaci), naivní test dává pokaždé jiný výsledek a je nespolehlivý. Používají se dvě strategie: buď se **ustálí zárodek (seed)** generátoru náhody, takže je posloupnost reprodukovatelná, nebo se ověřují **strukturální vlastnosti**, jež platí bez ohledu na náhodu (tvar výstupu, součty, rozsahy hodnot).

```python
def test_shlukovani_je_reprodukovatelne():
    a = KMeans(k=3, random_state=42).nauc(data).predikuj()
    b = KMeans(k=3, random_state=42).nauc(data).predikuj()
    assert (a == b).all()          # stejný seed → stejný výsledek
```

> **Rozcestník:** Problematika náhody a reprodukovatelnosti je rozsáhlá a má vlastní [samostatný materiál](../03-projekt-a-prostredi/reprodukovatelnost-seedy.md). Podstatné zde je, že ustálení zárodku ještě nezaručuje plný determinismus.

**Očekávané chyby.** Někdy je správným chováním právě vyvolání výjimky. Ověří se konstrukcí `pytest.raises`, která test označí za úspěšný pouze tehdy, nastane-li očekávaná výjimka:

```python
import pytest

def test_prazdny_vstup_vyvola_chybu():
    with pytest.raises(ValueError):
        prumer([])                 # prázdný vstup má vyvolat ValueError
```

**Čísla s plovoucí čárkou.** Hodnoty s plovoucí čárkou se kvůli konečné přesnosti neporovnávají na přesnou rovnost, nýbrž s tolerancí:

```python
assert abs(vysledek - 0.3) < 1e-9

import numpy as np
np.testing.assert_allclose(vysledek, ocekavano, atol=1e-6)   # pro pole
```

**Izolace jednotky.** Má-li být jednotka testována nezávisle na jiné součásti, na níž závisí, nahradí se tato součást jednoduchou náhradní implementací — tzv. **testovacím dvojníkem**. Test tím zůstává soustředěný na zkoumanou jednotku a nezávislý na správnosti okolí.

## 8. Nástroj pytest

V praxi se testy nespouštějí ručně, nýbrž testovacím nástrojem; nejrozšířenější je `pytest`. Po zadání příkazu

```bash
pytest
```

nástroj sám vyhledá a spustí testy podle konvence pojmenování: soubory `test_*.py`, třídy `Test*` a funkce `test_*`. Jednotlivý test lze spustit adresně:

```bash
pytest test_soubor.py::test_secti
```

Nad rámec spouštění poskytuje `pytest` řadu pomocných prostředků, z nichž mnohé jsou zapsány dekorátory; zde postačí ukázat jejich použití.

**Fixtury** (`@pytest.fixture`) připravují data či prostředí sdílené více testy. Test si o fixtura řekne tím, že uvede její jméno jako svůj parametr; `pytest` za něj dosadí návratovou hodnotu fixtury:

```python
import pytest

@pytest.fixture
def data():
    return [2, 4, 6]

def test_prumer(data):            # pytest dosadí za parametr návratovou hodnotu fixtury
    assert prumer(data) == 4
```

Obsahuje-li fixtura příkaz `yield`, provede se kód před ním jako **příprava** a kód za ním jako **úklid** po skončení testu. To se hodí u prostředků, které je nutné po použití uzavřít:

```python
@pytest.fixture
def spojeni():
    conn = otevri_spojeni()       # příprava — proběhne před testem
    yield conn                    # hodnota se předá testu
    conn.zavri()                  # úklid — proběhne po testu
```

Argumentem `scope` lze určit, jak často se fixtura vytváří; například `scope="module"` ji vytvoří jen jednou pro celý soubor, což se hodí u nákladné přípravy:

```python
@pytest.fixture(scope="module")
def velky_dataset():
    return nacti_velka_data()     # vytvoří se jednou pro všechny testy v souboru
```

**Parametrizace** (`@pytest.mark.parametrize`) spustí týž test opakovaně s různými sadami vstupů a očekávaných výsledků. Nahrazuje tak několik téměř shodných testů jediným:

```python
@pytest.mark.parametrize("vstup, ocekavano", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_druha_mocnina(vstup, ocekavano):
    assert vstup ** 2 == ocekavano
```

**Značky** (`@pytest.mark`) upravují, jak se s testem naloží. Značka `skipif` test za dané podmínky přeskočí, značka `xfail` označí test, o němž je předem známo, že selže (například kvůli dosud neopravené chybě):

```python
import sys

@pytest.mark.skipif(sys.version_info < (3, 11), reason="vyžaduje Python 3.11+")
def test_nove_rozhrani():
    ...

@pytest.mark.xfail(reason="známá dosud neopravená chyba")
def test_zatim_nefunguje():
    assert nedokoncena_funkce() == 42
```

**Pokrytí (coverage).** Nástroje pro měření pokrytí uvádějí, kolik kódu testy vůbec provedou.

> **Upozornění:** Pokrytí měří *dosah* testů, nikoli jejich *kvalitu*. Vysoké pokrytí doprovázené slabými ověřeními poskytuje falešnou jistotu — provést řádek kódu není totéž jako ověřit jeho správnost.

> **Další čtení:** dokumentace knihovny pytest, [docs.pytest.org](https://docs.pytest.org/).

## 9. Kdy a co netestovat

Testování má i svou míru; snaha otestovat vše vede k opačnému extrému.

- **Triviality** (například přímočaré čtení atributu) testovat netřeba.
- **Cizí kód** (jazyk, knihovny) se netestuje — předpokládá se jeho správnost.
- **Křehké testy vázané na vnitřní realizaci** se s každou úpravou implementace zbytečně rozbíjejí. Ověřuje se pozorovatelné chování a rozhraní, nikoli vnitřní podrobnosti.

Cílem je přiměřená sada testů ověřujících podstatné chování, nikoli maximální počet testů.

## 10. Shrnutí

Test je automatizované, opakovatelné ověření chování kódu; jeho náklad je jednorázový a předchází vývoji, kdežto užitek je průběžný — především možnost bezpečně upravovat kód. Příkaz `assert` je stavebním prvkem testu; samotný test je od holé kontroly odlišen tím, že jej systematicky spouští testovací nástroj. Přehledný test se člení podle vzoru Arrange–Act–Assert a ověřuje jedinou skutečnost; testovat lze funkce, třídy i celé řetězce. Obtížné případy — náhoda, očekávané chyby, čísla s plovoucí čárkou, izolace jednotky — mají ustálené postupy. Nástroj `pytest` testy vyhledává a spouští; pokrytí měří dosah, nikoli kvalitu. Tento text je vstupním rozcestníkem; hlubší poznání poskytují odkazované zdroje.
