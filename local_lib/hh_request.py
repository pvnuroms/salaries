#!/home/pupkin/projects/salaries/venv_salary/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
# from mail import Mail
from terminaltables import AsciiTable
from collections import OrderedDict


class Hh_Request:
    url = 'https://api.hh.ru/vacancies'
    """
    Работа с API HH
    Может сделать абстрактный класс, а от него унаследовать классы до конкретных API? 
    Нееет
    """
    def __init__(self, description, region, per_page = 100):
        self.description = description
        self.region = region
        self.url_parameter = {
            'text': self.description,
            'area': self.region,
            'describe_arguments': 'true'
        }
        self.per_page = per_page

    def get_page(self, page=0):
        params = {
        'text': self.description,
        'area': self.region,
        'page': page,
        'per_page': self.per_page,
        }
        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        print (req)
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    def get_vac_dict(self):
        """Серьезно, все в одну функцию запихал? А словарей точно два надо?
        Надо было сортировку отдельно сделать
        """
        vacansies_dict = {}
        dict_for_sort = {}
        for page in range(0, 20):
            jsObj = json.loads(self.get_page(page))
            page_result = jsObj.get('items')
            for work in page_result:
                print(work)
                id = work.get('id')
                salary = work.get('salary')
                print(salary)
                if not salary:
                    continue #Бойкотируем тех, кто не указывает З/п,
                    # salary = f'{0}-{0} HZ'
                    # salary_for_sort = 0
                else:
                    salary = work.get('salary')
                    print (salary)
                    salary = f"{salary.get('from')}-{salary.get('to')} {salary.get('currency')}"
                    salary_string = salary.split(' ')
                    salary_values = salary_string[0].split('-')
                    if 'None' in salary:
                        if salary_values[0] == 'None' and salary_values[1] != 'None':
                            salary_values[0] = salary_values[1]
                        elif salary_values[1] == 'None' and salary_values[0] != 'None':
                            salary_values[1] = salary_values[0]
                    salary = f'{salary_values[0]}-{salary_values[1]} {salary_string[-1]}'
                    salary_for_sort = salary_values[0]
                    dict_for_sort[id] = int(salary_for_sort)
                # print(work)
                name = work.get('name')
                employer = work.get('employer').get('name')
                deep_data = work.get('snippet').get('requirement')
                if not deep_data:
                    desc = 'NA'
                else:
                    desc = deep_data.replace('<highlighttext>', '').replace('</highlighttext>', '')
                ref = work.get('alternate_url')
                apply = work.get('apply_alternate_url')
                vacansies_dict[id] = [name, salary, employer, desc, ref, apply]
            if (jsObj['pages'] - page) <= 1:
                break
        sorted_tuples = sorted(dict_for_sort.items(), key=lambda item: item[1], reverse=True)
        # sorted_dict = {k: v for k, v in sorted_tuples}
        sorted_dict = OrderedDict()
        for k, v in sorted_tuples:
            sorted_dict[k] = vacansies_dict[k]
        self.sorted_dict = sorted_dict
        return sorted_dict


    def create_table_consol(self):
        """Получилось некрасиво, но это ничего, ведь функция оказалась бесполезна"""
        vacansies_dict = self.sorted_dict
        table_data = []
        table_data.append(['Должность', 'ЗП', 'Работодатель', 'Описание','Ссылка','Принять'])
        for key in vacansies_dict.keys():
            table_data.append(vacansies_dict[key])
        table = AsciiTable(table_data, self.description)
        return table.table

#TestZone
# if __name__ == '__main__':
#
#     requ = Hh_request('Python',1438)
#     result = requ.get_vac_dict()
#     text = ''
#     for id in result.keys():
#         # print (result[id])
#         value = '   |   '.join(result[id])
#         # print(value)
#         text =f'{text}\n\n{value}'
#     print (text)
#     mail = Mail('python', text, 'pvnuroms@mail.ru,')
#     mail.send_mail()
#     result = requ.create_table_consol()
#     # print (result)



