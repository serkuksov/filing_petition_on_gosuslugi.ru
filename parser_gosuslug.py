import datetime
import logging


def file_petition(number_ip: str, text_petition: str) -> dict:
    """Подает ходатайство на госулугах и возвращает номер и дату подачи ходатайства"""
    number_petition = 1
    date_petition = datetime.date.today()
    logging.info(f'Подано ходатайство № {number_petition}')
    return {'Дата отправки': date_petition,
            'Номер заявления': number_petition,
            }
