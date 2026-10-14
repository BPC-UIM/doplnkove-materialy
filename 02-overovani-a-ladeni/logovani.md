# Logování aplikací

*Výukový materiál — záznam průběhu programu pomocí modulu `logging`*

## 1. Motivace

Při vývoji se stav programu běžně zjišťuje příkazem `print`. Tento postup přestává dostačovat, jakmile program běží delší dobu nebo opakovaně. Uvažme trénink modelu trvající několik hodin, který v páté hodině selže: bez trvalého záznamu průběhu není z čeho zjistit, co selhání předcházelo. Rovněž ladění pomocí `print` vyžaduje řádky posléze ručně mazat a při dalším problému znovu vkládat.

**Logování** řeší obojí: poskytuje trvalý, strukturovaný záznam průběhu programu, který lze podle potřeby zapínat, vypínat a směrovat, aniž by se zasahovalo do kódu.

## 2. Print, log a výjimka: tři role

Příkaz `print`, logování a výjimky (`try`/`except`) nejsou tři způsoby téhož; plní tři různé úlohy:

- **`print`** je *okamžitý výstup pro člověka*. Nemá pojem závažnosti, směřuje pouze na obrazovku a nelze jej utlumit jinak než odstraněním řádku.
- **logování** je *záznam průběhu pro pozdější inspekci*. Rozlišuje závažnost, lze je nasměrovat na více míst zároveň a zapnout či vypnout beze změny kódu.
- **výjimky** jsou *řízení toku programu při selhání*. Mění to, co program **dělá**, nikoli to, co si zaznamenává.

### Úrovně závažnosti

Klíčovou předností logování oproti `print` jsou **úrovně závažnosti**. Každá úroveň má přiřazené **číslo**; to není jen orientační, nýbrž mechanismus, podle něhož se rozhoduje, co se zobrazí (viz níže).

| Úroveň | Číslo | Význam |
|---|---|---|
| `DEBUG` | 10 | podrobné informace potřebné při ladění (hodnoty proměnných, dílčí kroky) |
| `INFO` | 20 | potvrzení, že program probíhá podle očekávání (běh začal, model načten) |
| `WARNING` | 30 | nečekaný jev nebo blížící se problém; program pokračuje |
| `ERROR` | 40 | kvůli vážnějšímu problému se určitá operace nezdařila |
| `CRITICAL` | 50 | závažná chyba, program nemusí být schopen pokračovat |

Prahová úroveň je ve skutečnosti **číslo**: záznam se vypíše pouze tehdy, je-li jeho číslo **vyšší nebo rovné** prahu. Nastavíme-li práh na `WARNING` (30), projdou záznamy 30, 40 a 50, kdežto `INFO` (20) a `DEBUG` (10) se neobjeví. Ve vývoji se proto volí nízký práh (`DEBUG`) a vidí se vše, v provozu vysoký (`WARNING`) a vidí se jen podstatné — **bez mazání jediného řádku**.

> **Rozdíl mezi `INFO` a `WARNING`** nespočívá v „síle", nýbrž v účelu. `INFO` zaznamenává běžný, očekávaný průběh, který se v provozu zpravidla utlumuje (například „epocha 3 dokončena"). `WARNING` naopak označuje skutečnost, o níž je žádoucí vědět i tehdy, je-li běžný průběh utlumen (například „konfigurace neúplná, použita náhradní hodnota"). Orientační pravidlo: lze-li záznam v provozu bez následků pominout, náleží úrovni `INFO`; má-li upozorňovat na možný problém, náleží úrovni `WARNING`.

Z toho plyne nutná **kázeň ve volbě úrovní**: je-li vše na úrovni `INFO`, přestává být cokoli podstatné a smysl úrovní se ztrácí.

### Kde se log potkává s výjimkou

Logování a výjimky nejsou konkurenti; scházejí se právě v okamžiku selhání. Výjimka rozhodne, **co program udělá**, logování zaznamená, **že a s jakým kontextem** k selhání došlo:

```python
try:
    model = nacti_model(cesta)
except FileNotFoundError:
    logger.exception("Model se nepodařilo načíst z %s", cesta)  # zaznamená i výpis zásobníku
    raise                                                         # a rozhodne o toku programu
```

Metoda `logger.exception` zaznamená kromě zprávy i výpis zásobníku (traceback), což je při ladění selhání zásadní.

> **Poznámka:** Argumenty se do zprávy vkládají zástupnými znaky (`%s`), nikoli spojováním řetězců. Formátování se pak provede pouze tehdy, je-li záznam skutečně vypisován, což šetří výpočetní čas u utlumených úrovní.

Logování se vyplatí u všeho, co běží déle než okamžik nebo opakovaně. U krátkého jednorázového skriptu je `print` naopak zcela přiměřený; logování by zde bylo zbytečnou zátěží.

## 3. Vnitřní uspořádání: logger, handler, formatter

Modul `logging` se skládá ze tří součástí. Projděme je jednu po druhé, protože právě jejich záměna bývá zdrojem nedorozumění.

### Logger — kdo zaznamenává

Logger je objekt, který se v kódu volá. V každém modulu se získává podle jména modulu:

```python
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info("Trénink zahájen")
```

Použití pojmenovaného loggeru je vhodnější než přímé volání `logging.info(...)`, které sahá na tzv. **kořenový logger**. Pojmenované loggery umožňují cíleně utlumit záznamy jednotlivé knihovny produkující nadměrné množství výstupu a ponechat přitom v platnosti záznamy vlastního kódu — s kořenovým loggerem to možné není.

### Handler — kam záznam směřuje

Handler určuje cíl záznamu. Jeden logger jich může mít **více současně**, každý s vlastní prahovou úrovní. Nejčastější typy:

**`StreamHandler` — výstup na obrazovku.** Použije se pro průběžné sledování za běhu.

```python
konzole = logging.StreamHandler()
konzole.setLevel(logging.INFO)
```

**`FileHandler` — výstup do jednoho souboru.** Soubor však roste neomezeně; pro dlouhé nebo opakované běhy je proto vhodnější rotace (viz dále).

```python
soubor = logging.FileHandler("logs/run.log")
```

**`RotatingFileHandler` — rotace podle velikosti.** Této součásti je vhodné věnovat bližší pozornost. Handler zapisuje do souboru, dokud nedosáhne zadané velikosti (`maxBytes`); poté soubor **přejmenuje** a založí nový. Uchovává zadaný počet starších souborů (`backupCount`), nejstarší při dalším překročení smaže.

```python
from logging.handlers import RotatingFileHandler
soubor = RotatingFileHandler("logs/run.log", maxBytes=1_000_000, backupCount=5)
```

Ve složce `logs/` pak fyzicky vzniká:

```text
logs/run.log        <- aktuální, právě se do něj zapisuje
logs/run.log.1      <- předchozí
logs/run.log.2
logs/run.log.3
logs/run.log.4
logs/run.log.5      <- nejstarší; při dalším překročení se smaže
```

*Výhoda:* soubory nikdy nezaberou více než přibližně `maxBytes × (backupCount + 1)`, takže log nezaplní disk, a přitom zůstává zachována nedávná historie. *Kdy použít:* u procesů, které běží dlouho nebo trvale a produkují mnoho záznamů.

**`TimedRotatingFileHandler` — rotace podle času.** Nový soubor vzniká v pravidelném intervalu (například o půlnoci). *Kdy použít:* je-li třeba záznamy členit podle dní a snadno dohledat „log ze včerejška".

```python
from logging.handlers import TimedRotatingFileHandler
soubor = TimedRotatingFileHandler("logs/run.log", when="midnight", backupCount=7)
```

### Formatter — jak záznam vypadá

Formatter určuje podobu každého řádku pomocí zástupných polí. Připojuje se k handleru:

```python
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
konzole.setFormatter(formatter)
```

Nejužitečnější pole jsou `%(asctime)s` (čas), `%(name)s` (jméno loggeru), `%(levelname)s` (úroveň) a `%(message)s` (vlastní text). Výše uvedený formát vytvoří řádek tvaru:

```text
2026-08-24 14:32:05,123 | __main__ | INFO | Trénink zahájen
```

### Tok záznamu a dvě klasické nefunkčnosti

Záznam prochází cestou: logger → jeho handlery → každý handler jej naformátuje a odešle na své místo.

> **Upozornění:** První pokus o konfiguraci logování nejčastěji selže jedním ze dvou způsobů:
> - **Nic se nezobrazí.** Prahová úroveň je vyšší než úroveň záznamu (výchozí úroveň kořenového loggeru je `WARNING`, takže `INFO` a `DEBUG` se bez snížení úrovně neobjeví).
> - **Vše se zobrazí dvakrát.** Handler je připojen jak k vlastnímu loggeru, tak (typicky vlivem propagace) i ke kořenovému. Řeší se konfigurací na jediném místě, nebo vypnutím propagace: `logger.propagate = False`.

## 4. Rozumné ukládání logů

Nasměrování logů do souboru vyžaduje řád, jinak vznikne jediný nepřehledný soubor, v němž nelze nic dohledat.

**Umístění.** Logy patří do vlastní složky (`logs/`) mimo systém správy verzí — tedy do `.gitignore`, obdobně jako soubor `.env` s citlivými údaji.

**Členění.** Vedle rotace podle velikosti či času (viz kapitola 3) je ve výzkumném kontextu často nejpřehlednější **jeden log na jeden běh**, pojmenovaný časem nebo identifikátorem experimentu a uložený vedle příslušného modelu. Návrat k dřívějšímu experimentu je pak snadný.

### Co do logu patří a co nikoli

Do logu patří *co se stalo a dostatek kontextu, aby podle toho bylo možné jednat*: identifikace běhu, použitá konfigurace, klíčové metriky, učiněná rozhodnutí. Každá zpráva má být sama o sobě srozumitelná a snadno vyhledatelná.

Do logu naopak **nepatří**:

- **Citlivé údaje** — hesla, přístupové klíče, tokeny. Logy se sdílejí a přeposílají; tajný údaj v logu je nutné považovat za vyzrazený. (Souvislost s oddělením tajemství do `.env`.)
- **Osobní data** — z důvodu ochrany soukromí.
- **Rozsáhlé objekty** — celé datové struktury či tenzory. Zaznamenává se jejich tvar a několik statistik, nikoli obsah.
- **Záznamy v těsné smyčce** — logování v cyklu přes velké množství prvků zahltí výstup a zpomalí program. Zaznamenávají se milníky, nikoli každý krok.

> **Upozornění:** Zachytit výjimku a pouze ji potichu zaznamenat na nízké úrovni, aniž by se cokoli vyřešilo, je chybný vzor. Výjimku je třeba buď zpracovat, nebo propustit dál — nikoli předstírat, že nenastala.

## 5. Praktické příklady

Následující tři příklady postupují od nejjednoduššího spuštění ke skutečnému nastavení. U každého je uvedeno, co přesně vznikne na výstupu.

### 5.1 Jak začít — nejjednodušší možné logování

Nejrychlejší začátek zajistí funkce `basicConfig`, která nastaví kořenový logger jediným voláním. Je to vhodné pro první seznámení a pro malé skripty:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

logger.debug("Podrobnost pro ladění")     # NEzobrazí se — práh je INFO (20), DEBUG je 10
logger.info("Zahájení běhu")
logger.warning("Konfigurace neúplná, použity výchozí hodnoty")
```

Na obrazovce se objeví (řádek s `DEBUG` chybí, protože nedosáhl prahu):

```text
2026-08-24 14:32:05,123 | INFO | Zahájení běhu
2026-08-24 14:32:05,124 | WARNING | Konfigurace neúplná, použity výchozí hodnoty
```

### 5.2 Dva výstupy s různou úrovní

Jde o nejčastější nastavení v praxi a zároveň o hlavní důvod, proč se logování používá: **týž kód posílá přehledný výstup na obrazovku a současně úplný záznam do souboru**. Obrazovka zobrazuje pouze podstatné záznamy (`INFO` a výše), soubor uchovává i podrobnosti (`DEBUG` a výše).

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)             # logger propustí vše od DEBUG výše
logger.propagate = False                   # zamezí dvojímu výpisu přes kořenový logger

formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

konzole = logging.StreamHandler()          # obrazovka: jen INFO a výše
konzole.setLevel(logging.INFO)
konzole.setFormatter(formatter)

soubor = RotatingFileHandler("logs/run.log", maxBytes=1_000_000, backupCount=5)
soubor.setLevel(logging.DEBUG)             # soubor: vše od DEBUG
soubor.setFormatter(formatter)

logger.addHandler(konzole)
logger.addHandler(soubor)

logger.debug("Načteno 1024 vzorků")
logger.info("Trénink zahájen")
logger.warning("Nízká přesnost na validační množině")
```

Na **obrazovce** se objeví pouze dva řádky (`DEBUG` chybí):

```text
2026-08-24 14:32:05 | __main__ | INFO | Trénink zahájen
2026-08-24 14:32:07 | __main__ | WARNING | Nízká přesnost na validační množině
```

V **souboru `logs/run.log`** je záznam úplný, včetně `DEBUG`:

```text
2026-08-24 14:32:05 | __main__ | DEBUG | Načteno 1024 vzorků
2026-08-24 14:32:05 | __main__ | INFO | Trénink zahájen
2026-08-24 14:32:07 | __main__ | WARNING | Nízká přesnost na validační množině
```

### 5.3 Záznam selhání

V bloku `except` se použije `logger.exception`, jenž k záznamu automaticky připojí výpis zásobníku:

```python
try:
    vysledek = 10 / 0
except ZeroDivisionError:
    logger.exception("Výpočet selhal")
```

Ve výstupu se objeví záznam úrovně `ERROR` následovaný výpisem zásobníku, z něhož je patrné místo chyby:

```text
2026-08-24 14:32:09 | __main__ | ERROR | Výpočet selhal
Traceback (most recent call last):
  File "trenink.py", line 42, in <module>
    vysledek = 10 / 0
ZeroDivisionError: division by zero
```

## 6. Shrnutí a doporučený začátek

Příkaz `print` je okamžitý výstup, výjimka je řízení toku, log je trvalý záznam. Logování se vyplatí u dlouhých a opakovaných běhů; jeho hlavní předností jsou úrovně závažnosti, díky nimž se rozsah výstupu řídí jediným nastavením bez mazání kódu. Vnitřně je tvoří logger (kdo), handler (kam) a formatter (jak).

**Jak začít v praxi:** Pro první krok postačí `basicConfig` (příklad 5.1). Jakmile je třeba uchovat úplný záznam běhu, volí se dvojice handlerů — obrazovka s úrovní `INFO` a rotující soubor s úrovní `DEBUG` (příklad 5.2). V každém modulu se používá `logging.getLogger(__name__)`, logy se ukládají do složky mimo správu verzí a nesmějí obsahovat citlivé údaje.
