"""
conftest.py: Šestý projekt do Engeto Akademie Tester s Pythonem

author: Josef Věrovský
email: pepa.verovsky@seznam.cz / josef.verovsky@outlook.com
"""

import pytest
from playwright.sync_api import sync_playwright


SAUCE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


# Fixture "browser" vytvoří instanci prohlížeče, která bude platná pro celou testovací session
@pytest.fixture(scope="session")  # scope="session" znamená, že se spustí jen jednou pro všechny testy
def browser():
    # Spuštění Playwrightu
    with sync_playwright() as p:
        # Spuštění Chromium prohlížeče
        browser = p.chromium.launch()
        # Předáme prohlížeč testům
        yield browser
        # Po dokončení všech testů zavřeme prohlížeč
        browser.close()


# Fixture "page" vytvoří novou prázdnou záložku (kontext) pro každý test zvlášť
@pytest.fixture(scope="function")  # scope="function" = spustí se pro každý test znovu
def page(browser):
    # Vytvoření nového kontextu (izolované prostředí pro cookies, local storage atd.)
    context = browser.new_context()
    # Otevření nové stránky v tomto kontextu
    page = context.new_page()
    # Načtení úvodní stránky e-shopu
    page.goto(SAUCE_URL)
    # Předání stránky testu
    yield page
    # Po dokončení testu zavření kontextu (ukončí se i stránka)
    context.close()


# Fixture "logged_in_page" je rozšíření fixture "page"
# Udělá to, že po otevření stránky se rovnou přihlásí
@pytest.fixture(scope="function")
def logged_in_page(page):
    # Vyplnění uživatelského jména (CSS selektor pro input username)
    page.fill("input[data-test='username']", USERNAME)
    # Vyplnění hesla (CSS selektor pro input password)
    page.fill("input[data-test='password']", PASSWORD)
    # Kliknutí na tlačítko pro login
    page.click("input[data-test='login-button']")
    # Počká, dokud se neobjeví nadpis "Products" – znamená to, že login proběhl úspěšně
    page.wait_for_selector("span.title")
    # Vrátí již přihlášenou stránku testu
    return page
