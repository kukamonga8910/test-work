import openpyxl
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import keyboard


# Путь к файлу xlsx
FilePaths = '\\\luna\\public\\OFFICE\\CS-DEP\\private_folders\\AGremilova\\ЭДО\\'
FileXmlName = ''
# Товары
product = []
# Модель
model = []
# количество
number = []
# Еденица измерения пример штук=шт
unit = []
# Цена
price = []
# Сумма
amount = []
# Расчитаная сумма товара с НДС 20%
amountNds = []
# Сумма налога
taxAmount = []
# Итоговая сумма документа
totalAmount = 0
# Итоговая сумма с расчетом НДС 20%
totalAmountNds = 0
# Сумма налога от Итоговой суммы
totalAmountTax = 0
# Счетчик
count = 1


def getFiles(filePaths):
    global FileXmlName 
    filesXlsx = None
    fileXml = None
    files = os.listdir(filePaths)
    files = [file for file in files if os.path.isfile(os.path.join(filePaths, file)) and 'NEW_' not in file]
    files_with_dates = [(file, os.path.getmtime(os.path.join(filePaths, file))) for file in files]
    files_with_dates.sort(key=lambda x: x[1], reverse=True)
    last_two_files = files_with_dates[:2]

    for file, timestamp in last_two_files:
        if file.endswith('.xlsx'):
            if file.startswith('~$'):
                print('Закройте пожалуйста файл xlsx...')
                exit()
            filesXlsx = os.path.join(filePaths, file)
        elif file.endswith('.xml'):
            FileXmlName = file
            fileXml = os.path.join(filePaths, file)
    retrievingDataFromXlsx(filesXlsx)
    createXml(fileXml)


# В данной функции получаем данные из файла и заполняем массивы
def retrievingDataFromXlsx(filesXlsx):
    wookbook = openpyxl.load_workbook(filesXlsx)
    worksheet = wookbook.active
    for i in range(1, worksheet.max_row):
        if worksheet['B' + str(i)].value == 'Наименование оборудования и Работ':
            for j in range(i+1, worksheet.max_row):
                if worksheet['B' + str(j)].value == None:
                    break
                product.append(worksheet['B' + str(j)].value)
                model.append(worksheet['F' + str(j)].value)
                number.append(worksheet['H' + str(j)].value)
                unit.append(worksheet['I' + str(j)].value)
                price.append(worksheet['J' + str(j)].value)
# Вызывыаем функцию для подсчета суммы товаров и итоговой суммы документа
    getTotal(number, price)

# Вданной функции получаю сумму товара и общую сумму документа 
def getTotal(number, price):
    global totalAmount
    global totalAmountNds
    global totalAmountTax

    for numbers, prices in zip(number, price):
        result = numbers * prices
        amount.append(result)

    totalAmount = sum(amount)
    totalAmountNds = totalAmount * 1.2
    totalAmountTax = totalAmountNds - totalAmount
    # totalAmount = totalAmount
    
    NdsTotal(amount)
        

# В данной функции происходит расчет ндс 20% и округление до копеек
def NdsTotal(amount):
    for amounts in amount:
        nds = amounts * 1.2
        taxAmounts = nds - amounts
        amountNds.append(nds)
        taxAmount.append(taxAmounts)

def createXml(fileXml):
    global count

    tree = ET.parse(fileXml)
    root = tree.getroot()

    document_node = root.find('.//Документ')

    svschet_fact_node = document_node.find('.//СвСчФакт')
    if svschet_fact_node is None:
        svschet_fact_node = ET.SubElement(document_node, 'СвСчФакт')

    for tablschfact in document_node.findall('ТаблСчФакт'):
        document_node.remove(tablschfact)

    newTable = ET.Element('ТаблСчФакт')
    index = list(document_node).index(svschet_fact_node) + 1

    for products, models, numbers, units, prices, amounts, amountsNds, taxAmounts in zip(product, model, number, unit, price, amount, amountNds, taxAmount):
        new_svedtov = ET.SubElement(newTable, 'СведТов', {
            'НомСтр': f"{count}",
            'НаимТов': f"{products}" + ' ' + f"{models}" if models != None else f'{products}',
            'ОКЕИ_Тов': "796",
            'КолТов': f"{numbers}",
            'ЦенаТов': f"{prices:.2f}",
            'СтТовБезНДС': f"{amounts:.2f}",
            'НалСт': "20%",
            'СтТовУчНал': f"{amountsNds:.2f}"
        })
        akziz = ET.SubElement(new_svedtov, 'Акциз')
        bezakziz = ET.SubElement(akziz, 'БезАкциз')
        bezakziz.text = 'без акциза'

        sumnal = ET.SubElement(new_svedtov, 'СумНал')
        sumnal_value = ET.SubElement(sumnal, 'СумНал')
        sumnal_value.text = f'{taxAmounts:.2f}'

        dopsvedtov = ET.SubElement(new_svedtov, 'ДопСведТов', {
            'НаимЕдИзм': f"{units}"
        })
        count = count + 1
    
    new_vsogoopl = ET.SubElement(newTable, 'ВсегоОпл', {
    'СтТовБезНДСВсего': f"{totalAmount:.2f}",
    'СтТовУчНалВсего': f"{totalAmountNds:.2f}"
    })
    sumnalvsego = ET.SubElement(new_vsogoopl, 'СумНалВсего')
    sumnal = ET.SubElement(sumnalvsego, 'СумНал')
    sumnal.text = f'{totalAmountTax:.2f}'
    kolnetto = ET.SubElement(new_vsogoopl, 'КолНеттоВс')
    kolnetto.text = '106.000'

    document_node.insert(index, newTable)


    # Сохраняем изменения в XML-файл
    tree.write(f'{FilePaths}' + 'NEW_' + f'{FileXmlName}', encoding='utf-8', xml_declaration=True)



getFiles(FilePaths)

print('XML файл успешно создан. Для закрытия программы нажмите любую клавишу.')

keyboard.read_event()

print("программа завершена")


