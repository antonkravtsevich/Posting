import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def select_in_select(browser, xpath_click, xpath_ui, string):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_click))
        )
        element.click()
        ui = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ui))
        )
        li_s = ui.find_elements_by_tag_name("li")
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


def login(username, password, browser):
    browser.find_element_by_xpath("//a[@id='add']").click()
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__email']/input[@id='email']").send_keys(username)
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__passwd']/input[@id='passwd']").send_keys(password)
    browser.find_element_by_xpath("//input[@id='login']").click()
    return browser


def posting(browser, all_data):
    for data in all_data:
        print(data['rus_name'])
        if(data['type'] == "select"):
            show_select(browser, data)
        if(data['type'] == "checkbox"):
            show_checkbox(browser, data)
        if(data['type'] == "input"):
            show_input(browser, data)


def show_select(browser, data):
    print(data['values'])
    input_data = str(input())
    xpath = data['xpath']
    xpath_ui = data['xpath_ui']
    print(xpath)
    select_in_select(browser, xpath, xpath_ui, input_data)


def show_checkbox(browser, data):
    print("y/n:")
    input_data = str(input())
    xpath = data['xpath']
    if (input_data == "y"):
        checkbox = browser.find_element_by_xpath(xpath)
        checkbox.cick()


def show_input(browser, data):
    print("Enter data:")
    input_data = str(input())
    xpath = data['xpath']
    input_elem = browser.find_element_by_xpath(xpath)
    input_elem.send_keys(input_data)


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


def choose_category(category_name, db, browser):
    not_common = db['not_common']
    for elem in not_common:
        if (elem['category_name'] == category_name):
            category = elem
    category = category['category']
    selector0 = "//div[@class='ai_category']/b[@class='ai_category__label']"
    selector1 = category['category_selector1']
    selector2 = category['category_selector2']
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, selector0))
        )
        element.click()
        browser.find_element_by_xpath(selector1).click()
        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, selector2))
        )
        element.click()
        # choose type
        if(category['category_select']!='none'):
            select_in_select(browser, category['category_select'], category['category_ui'], category_name)

        checkbox = browser.find_element_by_xpath("//label[@class='package_none_label']/b")
        checkbox.click()
    finally:
        # browser.quit()
        i = 1


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(chrome_options=options)
    db_file = open('./db.json', 'r')
    db_source = db_file.read()
    db = json.loads(db_source)
    print("Выберите категорию: Планшеты и электронные книги, Мобильные телефоны, Телевизоры, Ноутбуки, Компьютеры")
    category_name = str(input())
    data = get_posting_data(db, category_name)
    start_url = "https://www.kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C"
    username = "user120895@gmail.com"
    password = "siniza314"
    browser.get(start_url)
    browser.save_screenshot('./screen1.png')
    # browser.find_element_by_xpath("//a[@class='joyride-close-tip']").click()
    browser = login(username, password, browser)
    choose_category(category_name, db, browser)
    posting(browser, data)
    print("wait")
    wait = input()

if __name__ == '__main__':
    main()