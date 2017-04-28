import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe')

'''
def start()
def si
def post(driver,type,name,info,author,params,cost):'''
driver.get('http://www.pulscen.by/')
wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'//span[@class="toolbar-link js-toolbar-link-enter"]')))
driver.find_element(By.XPATH, '//span[@class="toolbar-link js-toolbar-link-enter"]').click()
wait = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="session[email]"]')))
driver.find_element(By.XPATH, '//input[@name="session[email]"]').send_keys("user120895@gmail.com")
driver.find_element(By.XPATH, '//input[@name="session[password]"]').send_keys("siniza314")
driver.find_element(By.XPATH, '//input[@class="subm-"]').click()

wait = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="toolbar-link toolbar-link-button add-product js-ga-link"]')))
driver.find_element(By.XPATH, '//a[@class="toolbar-link toolbar-link-button add-product js-ga-link"]').click()
wait = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="product_name"]')))
driver.find_element(By.XPATH, '//input[@id="product_name"]').send_keys("комплюктер")
driver.find_element_by_id('product_announce').send_keys('Системный блок в компьютере является «главным». Если аккуратно открутить шурупы с его задней стенки, снять боковую панель и заглянуть внутрь, то лишь с виду его устройство покажется сложным. ')
wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Компьютеры, IT"]')))
driver.find_element(By.XPATH, '//a[text()="Компьютеры, IT"]').click()
wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Компьютеры"]')))
driver.find_element(By.XPATH, '//a[text()="Компьютеры"]').click()
wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Корпуса для компьютеров, системные блоки"]')))
driver.find_element(By.XPATH, '//a[text()="Корпуса для компьютеров, системные блоки"]').click()
wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Системный блок"]')))
driver.find_element(By.XPATH, '//a[text()=" Системный блок"]').click()
driver.find_element(By.XPATH, '//input[@id="product_trait_products_attributes_0_value"]').send_keys('ЯкобыINTEL')
driver.find_element(By.XPATH, '//input[@id="product_price"]').send_keys('220')
driver.find_element(By.XPATH, '//input[@id="article"]').send_keys('2128506')
driver.find_element(By.XPATH,'//select[@id="product_exists"]').click()
driver.find_element(By.XPATH,'//option[text()="в наличии"]').click()
driver.find_element(By.XPATH,'//select[@id="product_qty_measure_unit_id"]').click()

'''driver.findElement(By.id("cke_contents_textarea1")).sendKeys‌​("Test Text") '''

driver.find_element(By.XPATH,'//span[@class="cke_browser_gecko"]').send_keys('гуси долбятся в ноздрю')

wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//option[text()="шт."]')))
driver.find_element(By.XPATH,'//option[text()="шт."]').click()
driver.find_element(By.XPATH, '//input[@id="product_min_qty"]').send_keys('1')

'''название - <input class="uf-t js-length-check" data-counter="js-name-counter" id="product_name" maxlength="75" name="product[name]" size="75" type="text">'''
'''описание - <body style="border-width: 0;" class="editbox" spellcheck="false"><br></body>'''
'''компьютеры - <a href="#" class="go-link">Компьютеры, IT</a>'''





























'''БЕГИТЕ,ГЛУПЦЫ'''










