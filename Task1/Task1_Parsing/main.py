import analysis


def main():
    #получим разделение по грейдам среди аналитиков и саентистов
    analysts_grades = analysis.check_grades(analysis.analyst_vacancy_dframe('vacancies.json'))
    scientists_grades = analysis.check_grades(analysis.scientist_vacancy_dframe('vacancies.json'))
    
    #создадим итоговую таблицу с результатами анализа и отправим ее в файл
    res = analysis.result_df(analysts_grades, scientists_grades)
    res.to_json('result.json')
    print(res)
    print('\nВ директории обновлен(добавлен) файл с диаграммой.')
    
    #визуализируем результат с помощью круговых диаграмм и отправим их в файлы
    analysis.visualize(res)



if __name__ == "__main__":
    main()
    
    
