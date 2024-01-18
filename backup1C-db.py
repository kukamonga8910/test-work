from pathlib import Path
import shutil, os, glob

path = 'e:\\1C-DB'

def getFileAndDirName(path, count=1):
    name_list = []
    db_backup = []
    for name in os.listdir(path):
        name_list.append(name)
        print(f"{count}. {name}")
        count += 1
    choice = input('Введите номер базы данных для копирования базы: ').split(' ')
    for index in choice:
        db_backup.append(name_list[int(index) - 1])
    return backup_db(path, db_backup)

def backup_db(path, db_backup):
    for db in db_backup:
        dirname = input('Введите название новой директории: ')
        #os.mkdir(path+'\\'+dirname)
        new_dir = (path+'\\'+dirname)
        new_path = path+'\\'+db
        file_db = glob.glob(os.path.join(new_path, '*.1CD'))
        try:
            shutil.copytree(new_path+'\\'+'1Cv8Log', path+'\\'+dirname+'\\'+'1Cv8Log')
            for files in file_db:
                shutil.copy2(files, new_dir)
        except PermissionError as e:
            print(f"ошибка доступа: {e}")
        
        # for db_copy in os.listdir(new_path):
        #     shutil.copytree()




    # print('Level=' , level, 'Content:' , os.listdir(path))
    # for i in os.listdir(path, start=1):
    #     if os.path.isdir(path+'\\'+ i):
    #         print('Спускаемся', path + '\\' + i)
    #         getFileAndDir(path+'\\'+i, level+1)
    #         print('возвращаемся в', path)

getFileAndDirName(path)
