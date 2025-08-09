"""
test_saucedemo.py: Šestý projekt do Engeto Akademie Tester s Pythonem

author: Josef Věrovský
email: pepa.verovsky@seznam.cz / josef.verovsky@outlook.com
"""

# Nepotřebujeme importovat pytest, protože testy budou fungovat díky fixture z conftest.py
# Stačí jen napsat funkce začínající na "test_", pytest je sám najde

def test_login_success(logged_in_page):
    """Test úspěšného přihlášení do aplikace."""
    # Ověříme, že URL končí na "/inventory.html", což je stránka s produkty
    assert logged_in_page.url.endswith("/inventory.html")
    # Ověříme, že nadpis stránky je "Products"
    assert logged_in_page.inner_text("span.title") == "Products"


def test_menu_navigation(logged_in_page):
    """Test otevření menu a zobrazení všech položek."""
    # Klikneme na tlačítko "burger menu" (vlevo nahoře)
    logged_in_page.click("button#react-burger-menu-btn")
    # Počkáme, až se menu načte (má CSS třídu .bm-item-list)
    logged_in_page.wait_for_selector("nav.bm-item-list")
    # Načteme všechny texty odkazů v menu
    menu_items = logged_in_page.locator("nav.bm-item-list a").all_text_contents()
    # Seznam očekávaných položek v menu
    expected = ["All Items", "About", "Logout", "Reset App State"]
    # Ověříme, že každá očekávaná položka je skutečně v menu
    for item in expected:
        assert item in menu_items


def test_add_product_to_cart(logged_in_page):
    """Test přidání produktu do košíku."""
    # Klikneme na tlačítko "Add to cart" u produktu Sauce Labs Backpack
    logged_in_page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    # Ověříme, že ikona košíku obsahuje číslo "1" (počet položek)
    cart_badge = logged_in_page.inner_text("span.shopping_cart_badge")
    assert cart_badge == "1"


def test_cart_contents(logged_in_page):
    """Test zobrazení obsahu košíku."""
    # Nejprve přidáme produkt (jinak by košík byl prázdný)
    logged_in_page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    # Klikneme na ikonu košíku vpravo nahoře
    logged_in_page.click("a.shopping_cart_link")
    # Počkáme, až se stránka košíku načte (nadpis "Your Cart")
    logged_in_page.wait_for_selector("span.title")
    # Ověříme, že v košíku je položka "Sauce Labs Backpack"
    product_name = logged_in_page.inner_text("div.inventory_item_name")
    assert product_name == "Sauce Labs Backpack"


def test_checkout_process(logged_in_page):
    """Test celého procesu objednávky."""
    # Přidáme produkt do košíku
    logged_in_page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    # Otevřeme košík
    logged_in_page.click("a.shopping_cart_link")
    # Klikneme na tlačítko "Checkout"
    logged_in_page.click("button[data-test='checkout']")
    # Vyplníme jméno
    logged_in_page.fill("input[data-test='firstName']", "Test")
    # Vyplníme příjmení
    logged_in_page.fill("input[data-test='lastName']", "User")
    # Vyplníme PSČ
    logged_in_page.fill("input[data-test='postalCode']", "12345")
    # Klikneme na tlačítko "Continue"
    logged_in_page.click("input[data-test='continue']")
    # Ověříme, že se zobrazuje stránka s rekapitulací objednávky
    assert logged_in_page.inner_text("span.title") == "Checkout: Overview"
    # Klikneme na tlačítko "Finish"
    logged_in_page.click("button[data-test='finish']")
    # Ověříme, že se zobrazí potvrzení objednávky
    confirmation = logged_in_page.inner_text("h2.complete-header")
    assert confirmation == "Thank you for your order!"


def test_logout(logged_in_page):
    """Test odhlášení uživatele."""
    # Otevřeme menu
    logged_in_page.click("button#react-burger-menu-btn")
    # Počkáme, až se položka "Logout" objeví
    logged_in_page.wait_for_selector("a#logout_sidebar_link")
    # Klikneme na odhlášení
    logged_in_page.click("a#logout_sidebar_link")
    # Ověříme, že jsme zpět na login stránce (login tlačítko viditelné)
    assert logged_in_page.url == "https://www.saucedemo.com/"
