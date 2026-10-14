# Práce s gitem a GitHubem

*Výukový materiál — připomenutí verzování kódu pro grafická rozhraní (VS Code, GitHub Desktop, PyCharm)*

Tento text připomíná základy práce s gitem a GitHubem a poskytuje orientaci usnadňující zahájení práce v novém semestru. Popisuje operace a jejich smysl; jednotlivé úkony se provádějí v grafickém rozhraní, jehož konkrétní rozmístění tlačítek se mezi nástroji liší, avšak pojmenování operací je společné.

## 1. Proč verzovat kód

**Verzování** je průběžné zaznamenávání stavů kódu do historie, k níž se lze kdykoli vrátit. Řeší několik opakujících se potíží:

- **historie a návrat zpět** — každý zaznamenaný stav je dohledatelný; při chybné úpravě se lze vrátit k dřívější funkční verzi,
- **spolupráce** — více lidí může pracovat na témž projektu, aniž si navzájem přepisují soubory,
- **konec ručního zálohování** — odpadá vytváření, pojmenovávání a zasílání kopií souborů,
- **dohledatelnost změn** — z historie je patrné, co a kdy se změnilo.

## 2. Git versus GitHub

Tyto dva pojmy se často zaměňují, jde však o dvě různé věci:

- **Git** je *nástroj* pro verzování. Běží na počítači studenta, pracuje s lokálními soubory a funguje i bez připojení k internetu.
- **GitHub** je *hostovací služba* — místo na internetu, kam se ukládá kopie repozitáře, sdílí se s ostatními a spravuje přes webové rozhraní.

Git je samotným nástrojem verzování a je nezbytný; GitHub je jednou z možných služeb, kam lze umístit vzdálenou kopii repozitáře. Toto rozlišení je podstatné pro pochopení operace odeslání (push), při níž se lokální změny přenášejí na GitHub.

## 3. Uspořádání gitu: čtyři oblasti kódu

Toto uspořádání je jádrem celého tématu. Většina nejasností pramení z toho, že není zřejmé, ve které ze čtyř oblastí se kód právě nachází. Kód postupně prochází těmito oblastmi:

1. **Pracovní adresář** — soubory, které student právě upravuje.
2. **Připravená oblast (staging)** — změny vybrané k zaznamenání do nejbližšího záznamu.
3. **Lokální repozitář** — historie záznamů uložená na počítači studenta.
4. **Vzdálený repozitář** — kopie historie na GitHubu.

Kód mezi nimi přechází čtyřmi operacemi:

- **stage** (připravit) — přesune vybrané změny z pracovního adresáře do připravené oblasti,
- **commit** (zaznamenat) — uloží připravené změny jako záznam do lokálního repozitáře,
- **push** (odeslat) — přenese lokální záznamy do vzdáleného repozitáře,
- **pull** (stáhnout) — přenese záznamy ze vzdáleného repozitáře do lokálního.

> **Grafické rozhraní toto rozdělení zobrazuje přímo.** V panelu správy verzí (ve VS Code „Source Control", v GitHub Desktopu „Changes", v PyCharmu „Commit") jsou upravené soubory zpravidla rozděleny do dvou seznamů: nepřipravené změny (pracovní adresář) a připravené změny (staging). Přesun mezi nimi odpovídá operaci stage. Sledování těchto dvou seznamů je nejrychlejší způsob, jak zjistit, kde se kód nachází.

## 4. Získání repozitáře: clone

Prací se zpravidla začíná **naklonováním** (clone) vzdáleného repozitáře — vytvořením jeho lokální kopie na počítači. V grafickém rozhraní se zadá adresa (URL) repozitáře z GitHubu a cílová složka; nástroj stáhne obsah i celou historii.

Ve VS Code se úkon vyvolá příkazem „Git: Clone", v GitHub Desktopu volbou „File → Clone repository", v PyCharmu volbou „Get from VCS". Po naklonování je repozitář připraven k práci a je již propojen se svou vzdálenou kopií, čímž je určen cíl pozdějších operací push a pull.

## 5. Každodenní cyklus

Běžná práce probíhá v opakujícím se cyklu. Na jejím počátku je vhodné **stáhnout** (pull) případné změny ze vzdáleného repozitáře, aby lokální kopie byla aktuální. Poté následuje vlastní práce a její zaznamenání:

1. **pull** — na začátku práce se stáhnou aktuální změny.
2. Úprava souborů v pracovním adresáři.
3. **stage** — v panelu změn se vyberou soubory, které mají být součástí záznamu.
4. **commit** — připravené změny se s doprovodným sdělením uloží do lokálního repozitáře.
5. **push** — záznamy se odešlou do vzdáleného repozitáře.

V grafickém rozhraní odpovídá krok 3 označení souborů (tlačítko „+" či zaškrtnutí), krok 4 vyplnění pole se sdělením a stisku tlačítka „Commit" a krok 5 tlačítku „Push" (případně „Sync").

## 6. Táž práce v příkazové řádce

Ačkoli se v praxi pracuje převážně v grafickém rozhraní, tytéž úkony lze provést v příkazové řádce, kde je logika a posloupnost jednotlivých akcí zřetelnější — každý krok je samostatný pojmenovaný příkaz. Terminál je dostupný i uvnitř vývojových prostředí (PyCharm i VS Code jej mají zabudovaný).

Základní příkazy odpovídají operacím z předchozích kapitol:

```bash
git clone <adresa>          # získání repozitáře (clone)
git status                  # výpis stavu — ve které oblasti se soubory nacházejí
git add <soubor>            # příprava souboru (stage)
git commit -m "sdělení"     # zaznamenání připravených změn (commit)
git push                    # odeslání do vzdáleného repozitáře (push)
git pull                    # stažení ze vzdáleného repozitáře (pull)
```

Každodenní cyklus z kapitoly 5 pak v terminálu tvoří zřetelnou posloupnost:

```bash
git pull                    # 1. stažení aktuálního stavu
# ... úprava souborů ...
git status                  # 2. přehled změn a jejich stavu
git add soubor.py           # 3. příprava vybraných změn
git commit -m "Popis změny" # 4. zaznamenání
git push                    # 5. odeslání
```

Pro práci s větvemi slouží příkazy `git branch <jméno>` (založení větve), `git switch <jméno>` (přepnutí na větev) a `git merge <větev>` (sloučení uvedené větve do aktuální).

> **Doporučení:** Příkaz `git status` je vhodné používat často. Vypisuje, které soubory jsou upravené, které připravené a které dosud nezaznamenané, čímž přímo ukazuje rozdělení na čtyři oblasti z kapitoly 3.

## 7. Commity

**Commit** je zaznamenaný snímek připravených změn spolu s **doprovodným sdělením**, které popisuje, co záznam obsahuje. Sdělení je určeno především pro pozdější orientaci v historii, proto má být stručné a výstižné (například „Oprava výpočtu vzdálenosti", nikoli „změny").

Doporučuje se **zaznamenávat často a po malých krocích**. Menší, tematicky ucelené záznamy se snáze čtou, snáze se k nim vrací a v případě potíží přesněji ukážou, kde nastala změna.

## 8. Větve (branches)

**Větev** je samostatná linie vývoje. Umožňuje pracovat na určité změně odděleně, aniž by se zasahovalo do hlavní, funkční verze projektu. Hlavní větev se obvykle nazývá `main`.

Odbočení do vlastní větve je vhodné například při zkoušení nového postupu: dokud změna není hotová, hlavní větev zůstává nedotčená. V grafickém rozhraní se aktuální větev zobrazuje zpravidla ve stavovém řádku a přepíná či zakládá se z jeho nabídky.

## 9. Slučování (merge)

**Sloučení** (merge) spojí změny z jedné větve do druhé — typicky se dokončená práce z vedlejší větve sloučí zpět do větve `main`. Nedotýkají-li se změny týchž míst, proběhne sloučení samočinně. Dotýkají-li se, vzniká konflikt (viz kapitola 10).

V grafickém rozhraní se sloučení vyvolá z nabídky větví (volba typu „Merge into current branch").

## 10. Konflikty

Konflikt vzniká, když se na témže místě souboru setkají dvě různé změny a nástroj nedokáže sám rozhodnout, která platí. **Konflikt není chyba ani selhání** — je to dotaz nástroje, který ponechává rozhodnutí na člověku.

Místo konfliktu je v souboru vyznačeno značkami:

```text
<<<<<<< HEAD
vaše verze řádku
=======
příchozí verze řádku
>>>>>>> nazev_vetve
```

Část mezi `<<<<<<< HEAD` a `=======` je verze aktuální (vaše), část mezi `=======` a `>>>>>>>` je verze příchozí. Řešení spočívá ve výběru správné podoby, odstranění všech značek a zaznamenání výsledku.

Grafické rozhraní tento úkon usnadňuje: nabízí volby typu „Accept Current" (ponechat vaši verzi), „Accept Incoming" (ponechat příchozí) a „Accept Both" (ponechat obě), případně samostatný slučovací editor se dvěma verzemi vedle sebe. Po vyřešení je nutné soubor připravit (stage) a sloučení dokončit záznamem (commit).

## 11. Řešení častých obtíží

Následují nejčastější situace, které začátečníka znejistí, a jejich řešení. Zastřešující zásada zní: **před nevratným zásahem je vhodné se poradit; zaznamenaný (commitnutý) kód se v gitu jen málokdy skutečně ztratí.**

- **Odeslání (push) selhává, protože vzdálený repozitář obsahuje novější změny.** Někdo — nebo student sám z jiného počítače — mezitím odeslal změny. Řešením je nejprve stáhnout (pull), vyřešit případný konflikt a poté odeslat znovu.
- **Nechtěná úprava souboru, dosud nezaznamenaná.** Změny v pracovním adresáři lze zahodit volbou „Discard changes" a vrátit soubor do posledního zaznamenaného stavu.
- **Překlep ve sdělení nebo zapomenutý soubor v posledním záznamu.** Poslední záznam lze upravit volbou „Amend" (opravit poslední commit) — pozor, jen dokud nebyl odeslán.
- **Nejistota, kde se kód nachází.** Postačí otevřít panel změn a podle rozdělení na nepřipravené a připravené změny (kapitola 3) zjistit aktuální stav.

## 12. Co nepatří do repozitáře

Do verzování patří zdrojový kód, nikoli vše ostatní. K vyloučení vybraných souborů slouží soubor `.gitignore`, který obsahuje vzory názvů, jež git ignoruje. Do repozitáře zásadně **nepatří**:

- **citlivé údaje** — hesla, přístupové klíče, tokeny; jednou odeslaný údaj je nutné považovat za vyzrazený,
- **rozsáhlá data** — datové sady, obrázky, natrénované modely; git je určen pro text a kód, velké soubory repozitář zbytečně zvětšují,
- **odvozené a dočasné soubory** — virtuální prostředí, `__pycache__`, logy; jde o obsah, který lze kdykoli znovu vytvořit.

## 13. Shrnutí a odkazy

Git je nástroj pro verzování běžící lokálně, GitHub je hostovací služba pro vzdálené kopie. Kód prochází čtyřmi oblastmi — pracovní adresář, připravená oblast, lokální a vzdálený repozitář — a mezi nimi jej posouvají operace stage, commit, push a pull; grafické rozhraní tyto oblasti zobrazuje přímo. Běžná práce je opakující se smyčkou zakončenou odesláním. Větve oddělují rozdělanou práci, sloučení ji vrací zpět a konflikt je dotazem, který řeší člověk. Zaznamenaný kód se jen málokdy ztratí; před nevratným zásahem je vhodné se poradit.

> **Další čtení:** oficiální dokumentace gitu a volně dostupná kniha [Pro Git](https://git-scm.com/book), dokumentace GitHubu na [docs.github.com](https://docs.github.com).
