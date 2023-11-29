from src.utils import create_database, get_employers_data, save_data_to_database, update_database_config
from config import config
from src.DBManager import DBManager


def main():
    """
    Основная функция программы.
    """
    employer_companies = [1740,  # "Яндекс"
                          4181,  # "Банк ВТБ"
                          78638,  # "Тинькофф"
                          67611,  # "Тензор"
                          80,  # "Альфа-Банк"
                          9352463,  # "X5 Tech"
                          3529,  # "СБЕР"
                          2748,  # "Ростелеком"
                          733,  # "ЛАНИТ"
                          6093775  # "Aston"
                          ]

    print("Привет! Это программа для поиска вакансий на hh.ru\n"
          "Введите название базы данных, в которой будут находиться данные: ")
    database_name = input().lower()
    update_database_config()
    params = config()

    print("База данных создается, пожалуйста, подождите...")
    create_database(database_name, params)
    save_data_to_database(get_employers_data(employer_companies), database_name, params)
    user_manager = DBManager(database_name, params)

    while True:
        task = input(f'Для начала работы с программой выберете порядковый номер действия:\n'
                     f'1. Получение списка всех компаний и количества вакансий у каждой компании\n'
                     f'2. Получение списка всех вакансий с указанием названия компании, названия вакансии\n' 
                     f'   и зарплаты для каждой ссылки на вакансию\n'
                     f'3. Получение средней зарплаты по вакансиям\n'
                     f'4. Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                     f'5. Получение списка всех вакансий, в названии которых содержатся переданные в метод слова\n'
                     f'0. Завершение работы с программой\n')

        if task == "0":
            print('Завершение работы с программой.')
            break
        elif task == '1':
            print(user_manager.get_companies_and_vacancies_count())
            print()
        elif task == '2':
            print(user_manager.get_all_vacancies())
            print()
        elif task == '3':
            print(user_manager.get_avg_salary())
            print()
        elif task == '4':
            print(user_manager.get_vacancies_with_higher_salary())
            print()
        elif task == '5':
            keyword = input('Введите ключевое слово: ')
            answer = user_manager.get_vacancies_with_keyword(keyword)
            if answer:
                print(answer)
            else:
                print('Ничего не найдено.')
            print()
        else:
            print('Некорректный ввод. Повторите попытку.')


if __name__ == '__main__':
    main()
