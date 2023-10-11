import analysis


def main():
    vac = analysis.Analysis('vacancies.json')
    
    #распечатаем итоговую таблицу с результатами анализа и отправим ее в файл
    print(vac.result_df)
    vac.result_df.to_json('result.json')
    
    #визуализируем результат с помощью круговых диаграмм и отправим их в файлы
    print('\nВ директории обновлен(добавлен) файл с диаграммой.')
    vac.visualize()




if __name__ == "__main__":
    main()