import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# выбор пункта в ниспадающем списке
# browser - драйвер, xpath_click - xpath, который нужно кликнуть для того, чтобы ниспадающий список ниспал,
# xpath_ui - общий адрес ui, содержащий список li-шных пунктов меню, string - строка, пункт с которой нужно
# выбрать.
def select_in_select(browser, xpath_click, xpath_ui, string):
    try:
        # поиск элемента, по которому нужно кликнуть, чтобы появился список
        # с ожиданием!
        # action_chain = ActionChains(browser)
        element = WebDriverWait(browser, 100).until(
            EC.element_to_be_clickable((By.XPATH, xpath_click))
        )
        # action_chain.move_to_element_with_offset(element, 1, 1).click().perform()

        # script = 'document.getElementByXpath("'+xpath_click+'").click()'
        element.click()
        # browser.execute_script(script)
        # поиск ui с пунктами меню
        ui = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ui))
        )

        # выборка всех пунктов меню (тэг li) из ui
        li_s = ui.find_elements_by_tag_name("li")

        # поиск элемента, текст которого соответствует требуемому.
        right_elem = li_s[0]
        for li in li_s:
            div = li.find_element_by_tag_name("div")
            text = div.get_attribute("innerText")
            if (text.strip() == string):
                right_elem = div
        right_elem.click()
    finally:
        # browser.quit()
        i = 1

# функция входа в аккаунт
def login(username, password, browser):
    browser.find_element_by_xpath("//a[@id='add']").click()
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__email']/input[@id='email']").send_keys(username)
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__passwd']/input[@id='passwd']").send_keys(password)
    browser.find_element_by_xpath("//input[@id='login']").click()
    return browser


# функция выкладки. browser - драйвер, all-data - выборка данных, необходимых для выкладки
# (общие для всех категорий данные + данные для определенной категории)
# вызывает отдельные методы для выкладки различных элементов (лежат ниже)
def posting(browser, all_data):
    for data in all_data:
        print(data['rus_name'])
        if(data['type'] == "select"):
            show_select(browser, data)
        if(data['type'] == "checkbox"):
            show_checkbox(browser, data)
        if(data['type'] == "input"):
            show_input(browser, data)


# ввод данных в ниспадающий список
def show_select(browser, data):
    print(data['values'])
    input_data = str(input())
    xpath = data['xpath']
    xpath_ui = data['xpath_ui']
    print(xpath)
    select_in_select(browser, xpath, xpath_ui, input_data)


# вывод данных в чекбокс
def show_checkbox(browser, data):
    print("y/n:")
    input_data = str(input())
    xpath = data['xpath']
    if (input_data == "y"):
        checkbox = browser.find_element_by_xpath(xpath)
        checkbox.cick()


# ввод данных в инпут
def show_input(browser, data):
    print("Enter data:")
    input_data = str(input())
    xpath = data['xpath']
    input_elem = browser.find_element_by_xpath(xpath)
    input_elem.send_keys(input_data)


# выборка данных из db.json. Набираются общие для всех категорий данные + данные выбранной категории
def get_posting_data(db, category_name):
    common = db["common"]
    not_common = db["not_common"]
    for elem in not_common:
        if (elem['category_name'] == category_name):
            category = elem
    if (category['data']!="none"):
        all_data = common + category['data']
    else :
        all_data = common
    return all_data


# метод для перехода к нужной категории товара
def choose_category(category_name, db, browser):
    # получение информации о выбранной категории. xpath-ы, необходимые для выкладки объявления данные
    not_common = db['not_common']
    for elem in not_common:
        if (elem['category_name'] == category_name):
            category = elem
    category = category['category']
    # подборка селекторов для перехода к нужной категории.
    # селектор0 - для открытия списка категорий
    selector0 = "//div[@class='ai_category']/b[@class='ai_category__label']"
    # селектор1 - выбирает пункт в основном меню
    selector1 = category['category_selector1']
    # селектор2 = выбирает пункт во вторичном меню
    selector2 = category['category_selector2']
    # выбор данных
    try:
        # ожидание подгрузки элемента, который открывает ниспадающий список
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, selector0))
        )
        # открываем список
        element.click()
        # выбор нужных элементов меню
        browser.find_element_by_xpath(selector1).click()
        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector2))
        )
        element.click()
        # choose type
        if(category['category_select']!='none'):
            select_in_select(browser, category['category_select'], category['category_ui'], category_name)

        # выбор пункта выкладки "без продвижения"
        checkbox = browser.find_element_by_xpath("//label[@class='package_none_label']/b")
        checkbox.click()
    finally:
        # browser.quit()
        i = 1


def main():
    # установка опций браузера (открытие в полном размере окна)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(chrome_options=options)
    # открытие и обработка файла db.json
    db_file = open('./db.json', 'r')
    db_source = db_file.read()
    db = json.loads(db_source)
    print("Выберите категорию: ")
    print("Планшеты и электронные книги, Мобильные телефоны, Телевизоры, Ноутбуки, Компьютеры / системные блоки")
    category_name = str(input())
    data = get_posting_data(db, category_name)

    # начало выкладки
    start_url = "https://www.kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C"
    username = "user120895@gmail.com"
    password = "siniza314"
    browser.get(start_url)

    # вход в аккаунт
    browser = login(username, password, browser)

    # выбор категории
    choose_category(category_name, db, browser)

    # выкладка данных
    posting(browser, data)

    # ожидание
    print("wait")
    wait = input()

if __name__ == '__main__':
    main()