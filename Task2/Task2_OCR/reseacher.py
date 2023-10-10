from shiftlab_ocr.doc2text.reader import Reader as RusReader
import easyocr

import numpy as np
import pandas as pd
import json

import os
from glob import glob

import filehelper as fh



def folder_easyocr(path:str, file_name:str):
    """
    Для разбитого на картинки pdf, модель easyocr reader сканирует все страницы на наличие текста
    и записывает все даные в таблицу, которую возвращает.
    """
    reader = easyocr.Reader(['ru'])
    os.chdir(path)
    
    page_dfs = []
    for page in glob('*.png'):
        page_result = reader.readtext(page, detail=0, paragraph=True)
        page_df = pd.DataFrame(page_result, columns=['text'])
        page_df['page_number'] = int(page[(page.find('page'))+5:-4])
        page_dfs.append(page_df)
    pdf_df = pd.concat(page_dfs, ignore_index=True)
    pdf_df['file_name'] = f'{file_name}.pdf'
    
    os.chdir('..')
    
    return pdf_df



def folder_rus_cursive_ocr(path:str, file_name:str):
    """
    Для разбитого на картинки pdf, модель shiftlab rus handwriting reader сканирует все страницы
    на наличие текста и записывает все даные в таблицу, которую возвращает.
    """
    reader = RusReader()
    os.chdir(path)
    
    pdf_df = pd.DataFrame(columns=['text', 'page_number'])
    for page in glob('*.png'):
        page_result = reader.doc2text(page)
        pdf_df.loc[len(pdf_df.index)] = [page_result[0], int(page[(page.find('page'))+5:-4])]
    pdf_df['file_name'] = f'{file_name}.pdf'
    
    os.chdir('..')
    
    return pdf_df



def detect_str(row):
    res = ''.join(sym for sym in row['text'] if sym.isalpha()).lower()
    if len(res) > 3:
        return res
    else:
        return np.NaN
        
def cleaning_data(df:pd.DataFrame()):
    """
    Очищает таблицу от числовых символов, спецсимволов и от коротких(<4 символов) строк.
    """
    df['text'] = df.apply(lambda row: detect_str(row), axis=1)
    df.dropna(inplace=True, ignore_index=True)
    


def search_str(substring:str):
    """
    Поиск нужного слова ораганизован через просмотр json'а.
    """
    database = 'res_df.json'
    with open(database, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    marker = False #маркер о наличии или отсутствии в тексте нужного слова
    for item_number in data:
        fullstring = data[item_number]['text']
        
        if substring in fullstring:
            marker = True
            print(f'Строка "{substring}" найдена на странице {data[f"{item_number}"]["page_number"]} \
в файле {data[f"{item_number}"]["file_name"]}')
    
    if not marker:
        print(f'В файлах cтрока "{substring}" обнаружена не была.')



def get_text_from_pdfs():
    """
        Если были обнаружены pdf и прочитаны ocr-методом,
        то собрать все тексты со всех файлов в одну таблицу.
        Очистить данные от цифр и спецсимволов.
        Выполнить поиск слова.
    """
    df = []
    pdf_names = []
    for file in glob('*.pdf'): #пройтись по всем по очереди pdf
        file_name = file[:-4]
        if file_name[:4].find('hand') != -1: #если обнаружен признак рукописного текста
            #print(f'hand = {dir_name}')
            dir_name = fh.png_pages_from_pdf(file, file_name) #сконвертировать в pdf в картинки
            dir_df = folder_rus_cursive_ocr(dir_name, file_name) #считать с картинок текст
            fh.delete_folder(dir_name)
            df.append(dir_df)
            pdf_names.append(file)
        
        else:
            #print(f'print = {dir_name}')
            dir_name = fh.png_pages_from_pdf(file, file_name) #сконвертировать в pdf в картинки
            dir_df = folder_easyocr(dir_name, file_name) #считать с картинок текст
            fh.delete_folder(dir_name)
            df.append(dir_df)
            pdf_names.append(file)
    
    
    
    if df != []:
        res_df = pd.concat(df, ignore_index=True)
        
        cleaning_data(res_df)
        
        with open('res_df.json', 'w', encoding='utf-8') as file:
            res_df.to_json(file, orient='index', force_ascii=False)
        
        with open('pdf_names.txt', 'w', encoding='utf-8') as file:
            for item in pdf_names:
                file.write(f'{item}\n')
    
    else:
        print('There is not any pdf in directory.')
    






if __name__ == "__main__":
    print('65')
    
    """
    pdf_names = ['printed_text_scan.pdf', 'print848ed_text_scan.pdf', '454printed_text_scan.pdf']
    with open('pdf_names.txt', 'w', encoding='utf-8') as file:
        for item in pdf_names:
            file.write(f'{item}\n')
    
    names = []
    with open('pdf_names.txt', 'r', encoding='utf-8') as file:
        for line in file:
            names.append(line[:-1])

    
    
    
    get_text_from_pdfs()
    """
    
    
    
    
    
    
    
    