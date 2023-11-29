import psycopg2


class DBManager:
    """
    Класс для работы с базой данных.
    """

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT employer_name, COUNT(vacancy_id) '
                            'FROM employers '
                            'JOIN vacancies USING (employer_id) '
                            'GROUP BY employer_name;')

                rows = cur.fetchall()
                data = "\n".join([str(row) for row in rows])

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        conn.close()
        return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name, employer_name, salary, vacancies.vacancy_url '
                            'FROM vacancies '
                            'JOIN employers USING (employer_id);')

                rows = cur.fetchall()
                data = "\n".join([str(row) for row in rows])

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        conn.close()
        return data

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT employer_name, ROUND(AVG(salary)) AS average_salary '
                            'FROM employers '
                            'JOIN vacancies USING (employer_id) '
                            'GROUP BY employer_name;')

                rows = cur.fetchall()
                data = "\n".join([str(row) for row in rows])

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT * '
                            'FROM vacancies '
                            'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

                rows = cur.fetchall()
                data = "\n".join([str(row) for row in rows])

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, python.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(f"""
                            SELECT * 
                            FROM vacancies
                            WHERE lower(vacancy_name) LIKE '%{keyword}%'
                            OR lower(vacancy_name) LIKE '%{keyword}'
                            OR lower(vacancy_name) LIKE '{keyword}%'""")

                rows = cur.fetchall()
                data = "\n".join([str(row) for row in rows])

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        conn.close()
        return data
