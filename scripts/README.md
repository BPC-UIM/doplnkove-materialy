# Skripty pro tvorbu obrázků

Tato složka obsahuje skripty, které vytvářejí obrázky použité v doplňkových materiálech. Hotové obrázky jsou uloženy ve složce [`graphs/`](graphs/) a materiály je zobrazují přímo; ke čtení materiálů proto není spouštění skriptů zapotřebí. Skripty slouží k tomu, aby bylo zřejmé, jak obrázky vznikly, a aby je bylo možné upravit a znovu vytvořit.

## Obsah

| Skript | Materiál | Obrázky |
|---|---|---|
| [`bias_variance.py`](bias_variance.py) | [Kompromis mezi zkreslením a rozptylem](../04-strojove-uceni/bias-variance.md) | `bias-variance_terc.svg`, `bias-variance_u-krivka.svg` |
| [`optimalizatory.py`](optimalizatory.py) | [Optimalizátory neuronových sítí](../04-strojove-uceni/optimalizatory.md) | `optimalizatory_trajektorie.svg` |
| [`profilovani.py`](profilovani.py) | [Profilování a výkon](../02-overovani-a-ladeni/profilovani-vykon.md) | `profilovani_tridy-slozitosti.svg`, `profilovani_broadcasting.svg`, `profilovani_ulozeni-v-pameti.svg` |
| [`_styl.py`](_styl.py) | — | společný vzhled a ukládání obrázků |

## Opětovné vytvoření obrázků

Z kořenové složky repozitáře:

```bash
python -m venv .venv
.venv/Scripts/activate              # na Linuxu a macOS: source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/bias_variance.py
python scripts/optimalizatory.py
python scripts/profilovani.py
```

Obrázky se uloží do složky `scripts/graphs/` a přepíší předchozí verze. Verze knihoven jsou zafixované a náhodné prvky mají ustálený zárodek, takže opakované spuštění vytvoří shodné soubory; v systému správy verzí se proto projeví pouze skutečné změny obrázků.

## Zásady pro nové obrázky

- Každý materiál má nejvýše jeden skript, který vytváří všechny jeho obrázky; název obrázku začíná názvem materiálu.
- Na začátku skriptu se volá `nastav_styl()` a obrázek se ukládá funkcí `uloz()` z modulu `_styl.py`, čímž je zajištěn jednotný vzhled (bílé pozadí, barevná paleta rozlišitelná i při poruchách barvocitu, formát SVG).
- Pod obrázkem v materiálu se uvádí odkaz na skript, který jej vytváří.
