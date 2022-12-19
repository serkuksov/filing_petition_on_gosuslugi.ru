import logging
from exel_operations import get_not_filed_petitions, save_filed_petition_in_excel
from parser_gosuslug import file_petition


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
    logging.getLogger("pymorphy2").setLevel(logging.ERROR)


def file_petitions(not_filed_petitions: list[dict]):
    """Генератор поданных ходатайств который перебирает список словарей с параметрами ходатайства,
    вызывает функцию подачи ходатайства, получает ответ в виде параметров с
    датой отправки и номером заявления, и возвращает поданное ходатайство"""
    i = 1
    for petition in not_filed_petitions:
        params_petition = file_petition(number_ip=petition['Номер ИП'],
                                        text_petition=petition['Ходатайство'])
        filed_petition = petition | params_petition
        logging.info(f'Подано {i} ходатайств из {len(not_filed_petitions)}')
        i += 1
        yield filed_petition


def main():
    log()
    not_filed_petitions = get_not_filed_petitions()
    for filed_petition in file_petitions(not_filed_petitions=not_filed_petitions):
        save_filed_petition_in_excel(filed_petition)


if __name__ == '__main__':
    try:
        main()
    except:
        logging.exception()
