import os
import shutil

import fitz



def png_pages_from_pdf(path:str, file_name:str, needed_dpi:int=300):
    """
    Разбивает pdf файл на страницы в формате png для считывания потом с них текста методом OCR.
    """
    doc = fitz.open(path)
    
    #картинки страниц будем хранить в отдельной папке для последующего считывания с нее текста
    i = 1
    dir_name = file_name
    if os.path.isdir(dir_name):
        dir_name = f'{dir_name}_{i}'
    while os.path.isdir(dir_name):
        idx = dir_name.rfind('_')
        tmp = dir_name[idx:].replace(f'{i}', f'{i+1}')
        dir_name = ''.join([dir_name[:idx], tmp])
        i += 1
        
    os.mkdir(dir_name)
    os.chdir(dir_name)
    
    #сохраним все картинки
    for count, page in enumerate(doc):
        pixmap = page.get_pixmap(dpi=needed_dpi)
        pixmap.save(f'{dir_name}_page_{count+1}.png')
    
    doc.close()
    os.chdir('..')
    
    return dir_name
        


def delete_folder(path:str):
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  #remove the file
        else:
            shutil.rmtree(path) #remove dir and all contains
    except OSError as err:
        print(f'{err}. File {path} is not a file or dir.')







if __name__ == "__main__":
    fn = png_pages_from_pdf('printed_text_scan_1.pdf', 'printed_text_scan_1')

    
    
    
    
    