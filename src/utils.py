
import psycopg2
import requests


def filter_strings(string: str) -> str:
    """
    Принимает в качестве аргумента строку.
    Возвращает измененную строку без символов, прописанных в списке symbols.
    """

    symbols = ['\n', '<strong>', '\r', '</strong>', '</p>', '<p>', '</li>', '<li>',
               '<b>', '</b>', '<ul>', '<li>', '</li>', '<br />', '</ul>']

    for symbol in symbols:
        string = string.replace(symbol, '')

    return string


def filter_salary(salary):
    """Фильтрация заработной платы"""
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


def get_employers_data(employer_companies):
    """Получение данных о работодателях и вакансиях с помощью API hh.ru"""
    employers = []
    for employer in employer_companies:
        url_employer = f'https://api.hh.ru/employers/{employer}'
        hh_employers = requests.get(url_employer).json()
        hh_vacancies = requests.get(hh_employers['vacancies_url']).json()
        employers.append({
            'employer': hh_employers,
            'vacancies': hh_vacancies['items']
        })
    return employers


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц по данным из hh.ru"""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        # cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name.lower(), **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                description TEXT,
                employer_url VARCHAR NOT NULL,
                url_vacancies VARCHAR(100) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                salary INT,
                vacancy_url VARCHAR NOT NULL,
                description TEXT,
                employer_id INTEGER NOT NULL,
                FOREIGN KEY (employer_id) REFERENCES employers (employer_id)
                )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(employers: list[dict], database_name: str, params: dict):
    """Сохранение данных в базу данных"""

    conn = psycopg2.connect(dbname=database_name.lower(), **params)
    # conn.autocommit = True
    with conn.cursor() as cur:
        for employer in employers:
            cur.execute('INSERT INTO employers (employer_name, description, employer_url, url_vacancies)'
                        'VALUES (%s, %s, %s, %s)'
                        'returning employer_id',
                        (employer["employer"].get("name"),
                            filter_strings(employer["employer"].get("description")),
                            employer["employer"].get("alternate_url"),
                            employer["employer"].get("vacancies_url")))

            employer_id = cur.fetchone()[0]

            for vacancy in employer["vacancies"]:
                salary = filter_salary(vacancy["salary"])
                cur.execute('INSERT INTO vacancies'
                            '(employer_id, vacancy_name, salary, vacancy_url, description)'
                            'VALUES (%s, %s, %s, %s, %s)',
                            (employer_id, vacancy["name"], salary,
                                vacancy["alternate_url"], vacancy["snippet"].get("responsibility")))

    conn.commit()
    conn.close()


def update_database_config():
    """ Обновляет конфигурацию базы данных """
    config_data = {
        'host': input('Введите хост: '),
        'port': input('Введите порт: '),
        'user': input('Введите имя пользователя: '),
        'password': input('Введите пароль: ')
    }

    with open('database.ini', 'w') as config_file:
        config_file.write('[postgresql]\n')
        for key, value in config_data.items():
            config_file.write(f'{key}={value}\n')

    print('Данные успешно загружены!')
