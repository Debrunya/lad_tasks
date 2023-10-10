import sys
import os
from glob import glob

import reseacher as rsch





def main():
    argvars = sys.argv
    
    """
    Проверка на наличие результирующего файла с текстом.
    При отсутствии запустим его генерацию.
    """
    if not os.path.isfile('res_df.json'):
        rsch.get_text_from_pdfs()
        
    
    processed_pdf_names = [] #сканированные pdf-файлы
    if os.path.isfile('pdf_names.txt'):
        with open('pdf_names.txt', 'r', encoding='utf-8') as file:
            for line in file:
                processed_pdf_names.append(line[:-1])
    
    
    nonprocessed_pdf_names = [] #pdf-файлы в директории
    for file in glob('*.pdf'):
        nonprocessed_pdf_names.append(file)
    
    
    
    """
    Сравним названия отсканированных файлов с находящимися в директории для
    последующего запуска сканирования или поиска слова по результирующему json'у.
    """
    if set(processed_pdf_names) == set(nonprocessed_pdf_names):
        rsch.search_str(argvars[1].replace(' ', '').lower())
    
    else:
        rsch.get_text_from_pdfs()
        rsch.search_str(argvars[1].replace(' ', '').lower())
        
    


if __name__ == "__main__":
    main()
    
    
    
    
