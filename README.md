# Projekt_6 – Automatizované testy Saucedemo

## Popis projektu
Automatizované end-to-end testy demo e-shopu [Saucedemo](https://www.saucedemo.com/) pomocí Pythonu, pytest a Playwright.  
Testy pokrývají přihlášení, navigaci v menu, přidání produktu do košíku, kontrolu košíku, průchod objednávkou a odhlášení.

---

## Požadavky
- Python 3.8 a novější  
- Nainstalované závislosti podle `requirements.txt`  
- Playwright komponenty nainstalované (`playwright install`)

---

## Spuštění testů

1. Otevři terminál a přejdi do složky s projektem, kde jsou soubory `conftest.py` a `test_saucedemo.py`:
2. Otevři ve VSCode
3. Do terminálu napiš 'pytest test_saucedemo.py'

## Zajímavost
1. Pokudeš budeš chtít vidět co se na stránce děje pak uprav v conftest.py fixture s funkcí browser - přidáš headless=False, slow_mo=500

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()

2. Pokud chceš vidět detail jednotlivých testů pak v terminálu spusť testy pomocí 'pytest -v test_saucedemo.py'
