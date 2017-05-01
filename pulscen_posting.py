from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display


def login(username, password, browser):
    wait = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//span[@class="toolbar-link js-toolbar-link-enter"]')))
    browser.find_element(By.XPATH, '//span[@class="toolbar-link js-toolbar-link-enter"]').click()
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="session[email]"]')))
    browser.find_element(By.XPATH, '//input[@name="session[email]"]').send_keys(username)
    browser.find_element(By.XPATH, '//input[@name="session[password]"]').send_keys(password)
    browser.find_element(By.XPATH, '//input[@class="subm-"]').click()
    return browser


def choose_category(category_xpath, browser):
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='toolbar-part toolbar-part-right']/a[@class='toolbar-link toolbar-link-button add-product js-ga-link']")))
    browser.find_element(By.XPATH,  "//div[@class='toolbar-part toolbar-part-right']/a[@class='toolbar-link toolbar-link-button add-product js-ga-link']").click()
    wait = WebDriverWait(browser, 1000).until(EC.presence_of_element_located(
        (By.XPATH, category_xpath['category_selector1'])))
    browser.find_element(By.XPATH, category_xpath['category_selector1']).click()
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, category_xpath['category_selector2'])))
    browser.find_element(By.XPATH, category_xpath['category_selector2']).click()
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, category_xpath['category_selector3'])))
    browser.find_element(By.XPATH, category_xpath['category_selector3']).click()
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, category_xpath['category_selector4'])))
    browser.find_element(By.XPATH, category_xpath['category_selector4']).click()
    return browser


def data_entry_in_select(browser, data):
    browser.find_element(By.XPATH, data['xpath']).click()
    browser.find_element(By.XPATH, '//option[text()="'+data['value']+'"]').click()


def data_entry_in_input(browser, data):
    browser.find_element(By.XPATH, data['xpath']).send_keys(data['value'])


def posting(browser, posting_data):
    for data in posting_data:
        print(data['name'])
        if(data['type'] == "select"):
            data_entry_in_select(browser, data)
        if(data['type'] == "input"):
            data_entry_in_input(browser, data)


def confirm_posting(browser):
    # //input[@class='uf-sbm js-uf-sbm-add-product']
    browser.find_element(By.XPATH, "//input[@class='uf-sbm js-uf-sbm-add-product']").click()

def main(full_data):
    status = 1
    try:
        print('Start virtual display...')
        display = Display(visible=0, size=(1366, 768))
        display.start()
        print('Done.')

        print('Start posting '+str(full_data['category_xpath']['category_name']))

        print('Open browser... ')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(chrome_options=options)
        print('Done.')

        print('Get pulscen start page... ')
        start_url = 'http://www.pulscen.by/'
        browser.get(start_url)
        print('Done.')

        print('Authorization...')
        username = "user120895@gmail.com"
        password = "siniza314"
        browser = login(username, password, browser)
        print('Done.')

        print('Choose category...')
        browser = choose_category(category_xpath=full_data['category_xpath'],
                                  browser=browser)
        print('Done.')

        print('Posting...')
        posting(browser=browser,
                posting_data=full_data['posting_data'])
        print('Done.')

        print('Sending ads...')
        # i = input()
        confirm_posting(browser=browser)
        print('Done.')

        print('Posting finished. Clear memory...')
        browser.quit()
        display.stop()
        print('Done.')

    except Exception as e:
        print(e.__traceback__)
        status = 2
    finally:
        display.stop()
    return status
