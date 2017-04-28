import pymysql
import json
from kufar_posting import main as posting_on_kufar
from pulscen_posting import main as posting_on_puls
import time

marketplaces = {1: 'kufar', 2: 'pulsecen'}
tg_category = 'category'
tg_parameters = 'parametrs'

connection = pymysql.connect(host='188.166.93.46',
                             user='root',
                             password='A6qD5GH5Qy',
                             db='ap4up2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def execute_sql(script):
    try:
        with connection.cursor() as cursor:
            cursor.execute(script)
            connection.commit()
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


# marketplace - kufar, pulscen
# targert - category, parameters
# get xpath's
# if target 'category' - xpath to jump to neccessary category
# if target 'parameters' - xpath of adverts fields
def get_xpath(marketplace, target, id):
    return execute_sql("call getxpathfor" + marketplace + target + "(" + str(id) + ")")


def getcommonparametrsforpuls():
    return execute_sql('call getcommanparametrsforpulsecen()')


def getcommonparametrsforkufar():
    return execute_sql('call getcommanparametrsforkufar()')


def get_action():
    return execute_sql("call getaction()")


def get_advert_by_id(id):
    return execute_sql("SELECT * FROM ap4up2.app_adverts where advert_id="+str(id)+";")


def create_posting_data_for_kufar(data, common_parametrs, parametrs):
    res = []
    for elem in common_parametrs:
        for data_elem in data:
            if(str(elem['unify_id']) == data_elem['name']):
                temp_d = {'type': elem['type'],
                          'xpath': elem['xpath'],
                          'xpath_ui': elem['xpath_ui'],
                          'name': elem['name'],
                          'value': data_elem['value']}
                res.append(temp_d)
    if(parametrs):
        for elem in parametrs:
            for data_elem in data:
                if (str(elem['unify_id']) == data_elem['name']):
                    temp_d = {'type': elem['type'],
                              'xpath': elem['xpath'],
                              'xpath_ui': elem['xpath_ui'],
                              'name': elem['name'],
                              'value': data_elem['value']}
                    res.append(temp_d)
    return res


def create_posting_data_for_puls(data, common_parametrs, parametrs):
    res = []
    for elem in common_parametrs:
        for data_elem in data:
            if(str(elem['unify_id']) == data_elem['name']):
                temp_d = {'type': 'input',
                          'name': elem['name'],
                          'xpath': elem['xpath'],
                          'value': data_elem['value']}
                res.append(temp_d)
    if (parametrs):
        for elem in parametrs:
            for data_elem in data:
                if (str(elem['unify_id']) == data_elem['name']):
                    temp_d = {'type': 'input',
                              'name': elem['name'],
                              'xpath': elem['xpath'],
                              'value': data_elem['value']}
                    res.append(temp_d)
    return res


def kufar_processing(advert_category_id, advert_data):
    # получение xpath-ов для перехода к необходимой категории
    kufar_category_xpath = get_xpath(marketplace=marketplaces[1],
                                     target=tg_category,
                                     id=advert_category_id)[0]
    # получение xpath-ов общих параметров для площадки
    kufar_common_parameters_xpath = getcommonparametrsforkufar()
    # получение xpath-ов частных парамтеров для площадки
    kufar_parameters_xpath = get_xpath(marketplace=marketplaces[1],
                                       target=tg_parameters,
                                       id=advert_category_id)
    # получение json-а для выкладки данных на куфар
    kufar_posting_data = create_posting_data_for_kufar(data=advert_data,
                                                       common_parametrs=kufar_common_parameters_xpath,
                                                       parametrs=kufar_parameters_xpath)
    # получение полных данных для перехода к категории и выкладки данных
    kufar_all_data = {'category_xpath': kufar_category_xpath,
                      'posting_data': kufar_posting_data}
    # выкладка данных на куфар
    posting_on_kufar(full_data=kufar_all_data)


def pulscen_processing(advert_category_id, advert_data):
    # получение xpath-ов для перехода к необходимой категории
    puls_category_xpath = get_xpath(marketplace=marketplaces[2],
                                     target=tg_category,
                                     id=advert_category_id)[0]
    # получение xpath-ов общих параметров для площадки
    puls_common_parameters_xpath = getcommonparametrsforpuls()
    # получение xpath-ов частных парамтеров для площадки
    puls_parameters_xpath = get_xpath(marketplace=marketplaces[2],
                                       target=tg_parameters,
                                       id=advert_category_id)
    # получение json-а для выкладки данных на пульс

    print('puls_category_xpath')
    print(puls_category_xpath)
    print('puls_common_parameters_xpath')
    print(puls_common_parameters_xpath)
    print('puls_parametrs_xpath')
    print(puls_parameters_xpath)
    print('data')
    print(advert_data)
    puls_posting_data = create_posting_data_for_puls(data=advert_data,
                                                     common_parametrs=puls_common_parameters_xpath,
                                                     parametrs=puls_parameters_xpath)
    print('posting_data')
    print(puls_posting_data)

    # получение полных данных для перехода к категории и выкладки данных
    puls_all_data = {'category_xpath': puls_category_xpath,
                     'posting_data': puls_posting_data}
    # выкладка данных на куфар
    posting_on_puls(full_data=puls_all_data)


def action_processing(action):
    # id объявлеия
    id_advert = action['id_advert']
    # получение объявления
    advert = get_advert_by_id(id_advert)[0]
    # получение id категории
    advert_category_id = advert['advert_category_id']
    # получнеие id торговой площадки
    advert_market_id = advert['advert_market_id']
    # получение данных объявления
    advert_data = json.loads(advert['advert_data_json'])

    kufar_processing(advert_category_id=advert_category_id,
                    advert_data=advert_data)
    # pulscen_processing(advert_category_id=advert_category_id,
    #                    advert_data=advert_data)


def main():
    while(True):
        oldest_action = get_action()
        if(oldest_action):
            print('New ads found! Start posting...')
            action_processing(action=oldest_action[0])
        else:
            print('New ads not found. Wait...')
            time.sleep(5)

if __name__ == '__main__':
    main()
    connection.close()