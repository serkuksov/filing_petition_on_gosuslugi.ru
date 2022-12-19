import time
import logging
from selenium.webdriver.common.by import By
from parser.parser import Parser


class Parser_gosuslugi(Parser):
    def __init__(self, login, password, timeout=7, organization=0):
        url = 'https://www.gosuslugi.ru/'
        super().__init__(url=url, login=login, password=password, timeout=timeout)
        self.organization = organization
        self.authorization_user()

    def authorization_user(self):
        try:
            self.driver.find_element(By.XPATH, '//button/span[contains(text(), "Войти")]').click()
            time.sleep(self.timeout)
        except:
            logging.error('Ошибка парсинга!!! Не найдена кнопка входа')
            raise Exception()
        try:
            input_login = self.driver.find_element(By.XPATH, '//input[@id="login"]')
            input_login.click()
            input_login.clear()
            input_login.send_keys(self.login)
            input_password = self.driver.find_element(By.XPATH, '//input[@id="password"]')
            input_password.click()
            input_password.clear()
            input_password.send_keys(self.password)
            self.driver.find_element(By.XPATH, '//button[contains(text(), "Войти")]').click()
            time.sleep(self.timeout)
        except:
            logging.error('Ошибка парсинга!!! При вводе данных авторизации')
            raise Exception()
        # Проверка на наличия страницы войти как
        have_account_organization = self.driver.find_elements(By.XPATH, '//div/h3[contains(text(), "Войти как")]')
        if have_account_organization:
            list_organization = self.driver.find_elements(By.XPATH, '//button')
            try:
                try:
                    name = list_organization[self.organization].find_element(By.TAG_NAME, 'h4').text
                    list_organization[self.organization].click()
                    logging.info(f'Выполнен вход как {name}')
                except:
                    logging.error(f'Ошибка!!! Конфиг файл не правильно задан. Оганизации № {self.organization} нет"')
                    list_organization[0].click()
                    name = list_organization[0].find_element(By.TAG_NAME, 'h4').text
                    logging.info(f'Выполнен вход как {name}')
                time.sleep(self.timeout+3)
            except:
                logging.error('Ошибка парсинга!!! При выборе "Войти как"')
                raise Exception()
        elif self.organization > 0:
            logging.error('Ошибка конфигурации!!! Вы не можете войти как организация. '
                          'Таких прав нет у вашего аккаунта')
        logging.info(f'Авторизация прошла успешно')

