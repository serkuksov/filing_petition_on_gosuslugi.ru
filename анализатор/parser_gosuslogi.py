import datetime
import time
import logging
from selenium.webdriver.common.by import By
from parser.parser import Parser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class Parser_gosuslugi(Parser):
    def __init__(self, login, password, timeout=7, organization=0):
        """Инициализация класса. Параметр organization отвечает за порядковый номер
        юридического лица при авторизации (профили ИП, ООО и т.д.).
        В случае если organization=0 вход от имени частного лица"""
        url = 'https://www.gosuslugi.ru/'
        super().__init__(url=url, login=login, password=password, timeout=timeout)
        self.organization = organization
        self.authorization_user()

    def authorization_user(self):
        """Авторизация пользователя на сайте"""
        self.click_button(text_button='Войти')
        try:
            input_login = self.driver.find_element(By.XPATH, '//input[@id="login"]')
            input_login.click()
            input_login.clear()
            input_login.send_keys(self.login)
            input_password = self.driver.find_element(By.XPATH, '//input[@id="password"]')
            input_password.click()
            input_password.clear()
            input_password.send_keys(self.password)
            time.sleep(1)
            self.click_button(text_button='Войти')
        except:
            logging.error('Ошибка парсинга!!! При вводе данных авторизации')
            raise Exception()
        self.check_account_organization()

    def check_account_organization(self):
        """Проверка на наличия страницы войти как"""
        elm_account_organization = self.driver.find_elements(By.XPATH, '//div/h3[contains(text(), "Войти как")]')
        if elm_account_organization:
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
            except:
                logging.error('Ошибка парсинга!!! При выборе "Войти как"')
                raise Exception()
        elif self.organization > 0:
            logging.error('Ошибка конфигурации!!! Вы не можете войти как организация. '
                          'Таких прав нет у вашего аккаунта')
        logging.info(f'Авторизация прошла успешно')
        time.sleep(self.timeout + 3)

    def open_page_register_petition(self):
        """Открыть страницу для регистрации обращений"""
        url = 'https://www.gosuslugi.ru/600367/1/form'
        logging.info(f'Открываю страницу для регистрации обращения')
        self.open_new_page(url=url)
        elm = self.driver.find_elements(By.XPATH, f'//h4[contains(text(), "У вас есть черновик заявления")]')
        if elm:
            self.click_button(text_button='Начать заново')
            logging.info(f'Начинаю оформлять обращение с начала')
        time.sleep(self.timeout)

    def register_petition(self, number_ip: str, text_petition: str, path_file: str) -> dict:
        """Выполнить регистрацию обращения"""
        self.open_page_register_petition()
        self.click_button(text_button='Начать')
        self.click_button(text_button='Взыскатель')
        self.click_button(text_button='Иное')
        self.click_button(text_button='Подать ходатайство или объяснение')
        self.click_button(text_button='Ходатайство')
        self.click_button(text_button='Перейти к заявлению')
        for i in range(6):
            self.click_button(text_button='Верно')
        try:
            input_number_ip = self.driver.find_element(By.XPATH, '//input[@autocomplete="off"]')
        except NoSuchElementException:
            time.sleep(25)
            input_number_ip = self.driver.find_element(By.XPATH, '//input[@autocomplete="off"]')
        input_number_ip.click()
        input_number_ip.clear()
        input_number_ip.send_keys(number_ip)
        self.click_button(text_button='Продолжить')
        input_text = self.driver.find_element(By.XPATH, '//perfect-scrollbar/div/div[1]/div')
        input_text.click()
        input_text.clear()
        input_text.send_keys(text_petition)
        self.click_button(text_button='Продолжить')
        self.load_file(text_xpath_input='//epgu-constructor-uploader-button/button/../input', path_file=path_file)
        print("Подано")
        # self.click_button(text_button='Отправить заявление')
        # self.click_button(text_button='На главную')
        self.open_new_page('https://www.gosuslugi.ru/legal-entity')
        number_petition = self.get_number_petition()
        date_petition = datetime.date.today()
        logging.info(f'Подано ходатайство № {number_petition}')
        return {'Дата отправки': date_petition,
                'Номер заявления': number_petition,
                }

    def get_number_petition(self) -> str:
        """Получить номер нового зарегистрированного обращения"""
        self.open_page_new_petition()
        try:
            number_petition = self.driver.find_element(By.XPATH, '//section/h2/span[2]').text
        except NoSuchElementException:
            logging.error(f'Ошибка парсинга!!! Не найден элемент c номером заявления')
            raise NoSuchElementException()
        try:
            number_petition = int(number_petition[1:])
        except ValueError:
            number_petition = number_petition[1:]
        return number_petition

    def open_page_new_petition(self):
        """Открыть страницу последнего созданного обращения"""
        self.click_elm(xpath_elm='//a', text_elm='Все уведомления')
        try:
            text_xpath = f'//span[contains(text(), "Заявление получено ведомством")]/parent::span/parent::div/parent::a'
            elm = self.driver.find_elements(By.XPATH, text_xpath)
            elm[0].click()
            logging.info('Перехожу в карточку последнего обращения')
        except NoSuchElementException:
            logging.error(f'Ошибка парсинга!!! Не найден элемент нового заявления')
            raise NoSuchElementException()
        time.sleep(self.timeout)
