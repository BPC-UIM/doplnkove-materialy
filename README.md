# Doplňkové materiály

## 1. K čemu repozitář slouží

Tento repozitář obsahuje doplňkové studijní materiály ke kurzu BPC-UIM. Zaměřují se na programování jako řemeslo a na koncepty, které se při práci s kódem prakticky uplatní. Materiály nejsou povinnou ani zkoušenou látkou. Jsou navzájem samostatné a každý má vlastní příklady.

## 2. Mapa materiálů

### 00-git

Verzování kódu a spolupráce prostřednictvím gitu a GitHubu.

- [Práce s gitem a GitHubem](00-git/git-github-pripomenuti.md) — připomenutí základů verzování kódu pro grafická rozhraní.

### 01-psani-kodu

Zásady, které zlepšují čitelnost a kvalitu zdrojového kódu.

- [Kontrolní seznam pro psaní funkcí](01-psani-kodu/jak-psat-funkce.md) — zásady, podle nichž lze posoudit kvalitu jednotlivé funkce.
- [Typové anotace proměnných](01-psani-kodu/typovani-promennych.md) — účel a používání typových anotací v jazyce Python.
- [Základy objektově orientovaného programování](01-psani-kodu/zaklady-oop.md) — třídy a objekty v jazyce Python.

### 02-overovani-a-ladeni

Prostředky pro ověření správnosti kódu, hledání chyb a zlepšení výkonu.

- [Testování kódu](02-overovani-a-ladeni/testovani.md) — úvod do automatizovaného testování v jazyce Python.
- [Ladění kódu debuggerem](02-overovani-a-ladeni/ladeni-debugger.md) — hledání chyb pomocí debuggeru.
- [Logování aplikací](02-overovani-a-ladeni/logovani.md) — záznam průběhu programu pomocí modulu `logging`.
- [Profilování a výkon](02-overovani-a-ladeni/profilovani-vykon.md) — odhalení nevýkonného kódu a postupy jeho zrychlení.

### 03-projekt-a-prostredi

Organizace projektu a zajištění opakovatelného běhu kódu v různých prostředích.

- [Struktura projektu](03-projekt-a-prostredi/struktura-projektu.md) — organizace kódu od notebooku po balíček.
- [Konfigurační soubory](03-projekt-a-prostredi/konfiguracni-soubory.md) — správa konfigurace aplikací.
- [Reprodukovatelnost a nastavení seedů](03-projekt-a-prostredi/reprodukovatelnost-seedy.md) — zvládnutí náhodnosti v kódu strojového učení.
- [Kontejnerizace](03-projekt-a-prostredi/kontejnerizace.md) — kontejnery Docker a Apptainer pro přenositelné spouštění kódu.

### 04-strojove-uceni

Praktické aspekty strojového učení a práce s knihovnou PyTorch.

- [Kompromis mezi zkreslením a rozptylem](04-strojove-uceni/bias-variance.md) — projevy a ovlivnění kompromisu v praxi.
- [Optimalizátory neuronových sítí](04-strojove-uceni/optimalizatory.md) — rodina optimalizátorů za hranicí základního gradientního sestupu.
- [Infrastruktura PyTorche](04-strojove-uceni/pytorch-infrastruktura.md) — prostředky pro práci s daty, modely a tréninkem.

## 3. Kde začít

Doporučené pořadí čtení vychází z logiky témat: nejprve git, poté psaní kódu, ověřování a ladění, dále projekt a prostředí (v rámci něj nejprve struktura projektu) a nakonec strojové učení. Materiály lze číst i samostatně, podle aktuální potřeby.
