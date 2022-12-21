import json
import logging
import os

from exel_operations import get_not_filed_petitions, save_filed_petition_in_excel
from parser.parser_gosuslogi import Parser_gosuslugi


def log():
    """Логирование скрипта в консоль и файл"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        'log.txt', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    handler.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    logging.getLogger("selenium").setLevel(logging.ERROR)
    logging.getLogger("webdriver_manager").setLevel(logging.ERROR)


def get_config():
    try:
        with open('config.txt', 'r', encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error('Ошибка!!! Не удалось открыть файл конфигурации')
        raise FileNotFoundError
    list_config = list(config.keys())
    verification_list_config = [
        "LOGIN",
        "PASSWORD",
        "TIMEOUT",
        "ORGANIZATION",
        "NAME_FILE_ORDER",
        "NAME_EXEL",
    ]
    if list_config == verification_list_config:
        logging.info(f'Получены параметры конфигурации')
        return config
    else:
        logging.error('Ошибка!!! В файле конфигурации нет части настроек')
        raise ValueError()


def get_path_file(name_file: str) -> str:
    """Проверяет наличие файла в текущей директории запуска скрипта.
    Возвращает путь к файлу."""
    path_script = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_script, name_file)
    if not os.path.exists(path_file):
        logging.error(f'Не найден файл приказа с названием {name_file}')
        raise FileNotFoundError
    logging.info(f'Получен путь к файлу приказа')
    return path_file


def filing_petitions():
    """Функция для подачи ходатайств.
    Перебирает список словарей с параметрами ходатайства, прочитанный из эксель,
    вызывает функцию подачи ходатайства, получает ответ в виде параметров с
    датой отправки и номером заявления. Сохраняет данные в эксель"""
    config = get_config()
    login = config['LOGIN']
    password = config['PASSWORD']
    timeout = int(config['TIMEOUT'])
    organization = int(config['ORGANIZATION'])
    name_file = config['NAME_FILE_ORDER']
    name_excel = config['NAME_EXEL']
    not_filed_petitions = get_not_filed_petitions(name_excel=name_excel)
    if not not_filed_petitions:
        exit()
    if not_filed_petitions[0]['Номер ИП'] is None or not_filed_petitions[0]['Ходатайство'] is None:
        logging.error('В эксель задана пустая строка. Или введены не все параметры')
        exit()
    parser = Parser_gosuslugi(login=login,
                              password=password,
                              timeout=timeout,
                              organization=organization,
                              )
    path_file = get_path_file(name_file=name_file)
    i = 1
    for petition in not_filed_petitions:
        if petition['Номер ИП'] is None or petition['Ходатайство'] is None:
            logging.error('В эксель задана пустая строка. Или введены не все параметры')
            continue
        logging.info(f'Приступаю к подаче обращения {i}')
        params_petition = parser.register_petition(number_ip=petition['Номер ИП'],
                                                   text_petition=petition['Ходатайство'],
                                                   path_file=path_file)
        filed_petition = petition | params_petition
        logging.info(f'Подано {i} обращение из {len(not_filed_petitions)}')
        i += 1
        save_filed_petition_in_excel(filed_petition=filed_petition, name_excel=name_excel)


def main():
    log()
    filing_petitions()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        logging.exception(ex)
