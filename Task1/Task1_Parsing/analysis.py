import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def analyst_vacancy_dframe(file:str):
    df = pd.read_json(file)
    
    #ключевые слова поиска аналитиков данных
    analyst_keywords = r'(dat.*analy)|(дат.*аналит)|(аналит.*данны)|(данны.*анали)|(dat.*аналит)|(аналит)'
    
    #проверка на ключевые слова
    vac_list = df['vacancy_name'].apply(lambda x: re.search(analyst_keywords, str(x).lower()))
    
    #для каждой строки проверяем наличие слов в столбце vacancy_name (результат: True/False)
    itog = np.any(np.array([~vac_list.isnull()]), axis=0)
    
    #оставляем только те строки в таблице, по которым получен результат True
    new_df = df[itog]

    return new_df



def scientist_vacancy_dframe(file:str):
    df = pd.read_json(file)
    
    #ключевые слова поиска data-science специалистов
    scientist_keywords = r'(scien)|(dat.*engin)|(dat.*инжен)|(дат.*инжен)'
    
    #проверка на ключевые слова
    vac_list = df['vacancy_name'].apply(lambda x: re.search(scientist_keywords, str(x).lower()))
    
    #для каждой строки проверяем наличие слов в столбце vacancy_name (результат: True/False)
    itog = np.any(np.array([~vac_list.isnull()]), axis=0)
    
    #оставляем только те строки в таблице, по которым получен результат True
    new_df = df[itog]
    
    return new_df



def check_grades(df:pd.DataFrame()):
    """
    Анализирует количество вакансий по грейдам исходя из усредненного расчета опыта работы в области:
        опыт не требуется - джун
        1-3 года работы - мидл
        3-6 лет работы - синьор
        >6 лет работы - лид
    Подразумевается именно такие усредненные рамки из-за трех причин:
        возможности градации сайта hh.ru
        внутри каждой компании градация может не совпадать с остальными
        некоторые вакансии не имеют четкого обозначения грейда рекрутируемого
    """
    #ключевые слова разделения по grades
    grade_keywords = np.array(['(н.*треб)', '(1–3)', '(3–6)', '(более)'])
    
    #распределение по grades 
    grades_list = np.array([], dtype=np.int32)
    for keywords in grade_keywords:
        #проверка на ключевые слова
        grades = df['work_experience'].apply(lambda x: re.search(keywords, str(x).lower()))
        
        #для каждой строки проверяем наличие слов в столбце work_experience (результат: True/False)
        #и подсчитываем количество совпадений
        itog = np.sum(np.any(np.array([~grades.isnull()]), axis=0))
        grades_list = np.append(grades_list, itog)
    
    return grades_list



def result_df(an_grades:list, sci_grades:list):
    """
    Выводит результирующую табличку с количеством вакансий в разделении по грейдам
    """
    df = pd.DataFrame(np.array([an_grades, sci_grades]), index=['Analysts', 'Scientists'],
                      columns=['junior', 'middle', 'senior', 'lead'])
    
    return df



def visualize(df:pd.DataFrame()):
    total_vacancies = df.sum(axis=1) #количество вакансий по специальностям
    vacancies_np_arr = df.to_numpy() #табличка в представлении двумерного массива
    legend=['junior', 'middle', 'senior', 'lead']
    
    #конструируем фигуру и ее элементы
    fig = plt.figure(figsize=(14, 7))
    fig.canvas.manager.set_window_title('Графическое представление о кол-ве вакансий по направлениям и грейдам в Н. Новгороде')
    fig.suptitle('Графическое представление о кол-ве вакансий по направлениям и грейдам в Н. Новгороде', fontsize=18)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    
    
    #конструируем первую диаграмму для аналитиков
    ax1.set_title('Analysts', fontsize=16)
    ax1.pie(vacancies_np_arr[0], labels=legend, labeldistance=1.05, shadow=True, explode=[0.08, 0.05, 0.05, 0.1],
            wedgeprops={'edgecolor':'black', 'antialiased':True},
            autopct=lambda x: '{:.0f}'.format(x*total_vacancies[0]/100), pctdistance=0.8)
    ax1.legend()
    
    #конструируем вторую диаграмму для саентистов
    ax2.set_title('Scientists', fontsize=16)
    ax2.pie(vacancies_np_arr[1], labels=legend, labeldistance=1.05, shadow=True, explode=[0.08, 0.05, 0.05, 0.1],
            wedgeprops={'edgecolor':'black', 'antialiased':True},
            autopct=lambda x: '{:.0f}'.format(x*total_vacancies[1]/100), pctdistance=0.8)
    ax2.legend()

    #сохраняем картинку с результирующей визуализацией
    fig.savefig('result.png')



if __name__ == "__main__":
    df = analyst_vacancy_dframe('vacancies.json')
    rows_number = df.count()
    print(df)
    print(f'rows_number = {rows_number[0]}')

    an_grades = check_grades(df)
    print(an_grades)
    
    sci_grades = check_grades(scientist_vacancy_dframe('vacancies.json'))
    
    itog = result_df(an_grades, sci_grades)
    print(itog)
    
    visualize(itog)
    
    
    
    
    
    
    



