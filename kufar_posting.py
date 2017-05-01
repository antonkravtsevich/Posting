from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium.webdriver.common.action_chains import ActionChains

# функция входа в аккаунт
def login(username, password, browser):
    # wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    #     (By.XPATH, "//a[@id='add']")))
    browser.find_element_by_xpath("//a[@id='add']").click()
    # wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    #     (By.XPATH, "//fieldset[@class='form_login_fieldset form_login_fieldset__email']/input[@id='email']")))
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__email']/input[@id='email']").send_keys(username)
    browser.find_element_by_xpath("//fieldset[@class='form_login_fieldset form_login_fieldset__passwd']/input[@id='passwd']").send_keys(password)
    browser.find_element_by_xpath("//input[@id='login']").click()
    return browser


# выбор пункта в ниспадающем списке
# browser - драйвер, xpath_click - xpath, который нужно кликнуть для того, чтобы ниспадающий список ниспал,
# xpath_ui - общий адрес ui, содержащий список li-шных пунктов меню, string - строка, пункт с которой нужно
# выбрать.


def choice_item_in_select(browser, xpath_click, xpath_ui, string):
    action_chain = ActionChains(browser)
    element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_click))
    )

    browser.execute_script("arguments[0].click()", element)

    ui = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_ui))
    )

    li_s = ui.find_elements_by_tag_name("li")

    right_elem = li_s[0]
    for li in li_s:
        div = li.find_element_by_tag_name("div")
        text = div.get_attribute("innerText")
        if(text.strip() == string):
            right_elem = div

    action_chain.move_to_element(element).perform()
    right_elem.click()

'''
def choice_item_in_select(browser, xpath_click, xpath_ui, string):
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
'''

# метод для перехода к нужной категории товара
def choose_category(category_xpath, browser):
    # подборка селекторов для перехода к нужной категории.
    # селектор0 - для открытия списка категорий
    selector0 = "//div[@class='ai_category']/b[@class='ai_category__label']"
    # селектор1 - выбирает пункт в основном меню
    selector1 = category_xpath['category_selector1']
    # селектор2 = выбирает пункт во вторичном меню
    selector2 = category_xpath['category_selector2']
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
        if(category_xpath['category_select']!='none'):
            choice_item_in_select(browser, category_xpath['category_select'], category_xpath['category_ui'], category_xpath['category_name'])

        # выбор пункта выкладки "без продвижения"
        checkbox = browser.find_element_by_xpath("//label[@class='package_none_label']/b")
        checkbox.click()
    finally:
        # browser.quit()
        i = 1


# функция выкладки. browser - драйвер, all-data - выборка данных, необходимых для выкладки
# (общие для всех категорий данные + данные для определенной категории)
# вызывает отдельные методы для выкладки различных элементов (лежат ниже)
def posting(browser, posting_data):
    for data in posting_data:
        print(data['name'])
        if(data['type'] == "select"):
            data_entry_in_select(browser, data)
        if(data['type'] == "checkbox"):
            data_entry_in_checkbox(browser, data)
        if(data['type'] == "input"):
            data_entry_in_input(browser, data)


# ввод данных в ниспадающий список
def data_entry_in_select(browser, data):
    xpath = data['xpath']
    xpath_ui = data['xpath_ui']
    choice_item_in_select(browser, xpath, xpath_ui, data['value'])


# вывод данных в чекбокс
def data_entry_in_checkbox(browser, data):
    xpath = data['xpath']
    if (data['value'] == 'y'):
        checkbox = browser.find_element_by_xpath(xpath)
        checkbox.cick()


# ввод данных в инпут
def data_entry_in_input(browser, data):
    xpath = data['xpath']
    input_elem = browser.find_element_by_xpath(xpath)
    input_elem.send_keys(data['value'])

# отправка объявления на куфар
def confirm_posting(browser):
    validate_button = browser.find_element_by_xpath("//div[@class='form_data']/input[@id='validate'][2]")
    validate_button.click()


def main(full_data):

    print('Start virtual display...')
    display = Display(visible=0, size=(1366, 768))
    display.start()
    print('Done.')

    print('Start posting '+str(full_data['category_xpath']['category_name']))

    print('Open browser... ')
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1366, 768)
    print('Done.')

    print('Get kufar start page... ')
    browser.implicitly_wait(5)
    start_url = "https://www.kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C"
    browser.get(start_url)
    print('Implicity wait finish')
    print('Done.')

    print('Authorization...')
    username = "user120895@gmail.com"
    password = "siniza314"
    browser = login(username, password, browser)
    print('Done.')

    print('Choose category...')
    choose_category(category_xpath=full_data['category_xpath'],
                    browser=browser)
    print('Done.')

    print('Posting...')
    posting(browser=browser,
            posting_data=full_data['posting_data'])
    print('Done.')

    print('Sending ads...')
    # confirm_posting(browser=browser)
    print('Done.')

    print('Posting finished. Clear memory...')
    browser.quit()
    display.stop()
    print('Done.')
    print('Posting cycle finished.')
