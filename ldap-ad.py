from googletrans import Translator
import string, secrets, csv
from pyad import *
from ldap3 import Server, Connection, ALL_ATTRIBUTES, ALL, SUBTREE
from datetime import timedelta

# Создание Аккаунтов 
def generate_account(username):
    account = []
    for names in username.split(","):
        fullName = names.strip()
        firstnameRus, nameRus, lastnameRus = fullName.split()
        translator = Translator()
        EngFullName = translator.translate(fullName)
        firstnameEng, nameEng, lastnameEng = EngFullName.text.split()
        login_ad_kos = f"{firstnameEng}" + f"{nameEng[0]}" + f"{lastnameEng[0]}"
        login_ad_msk = f"{nameEng[0]}." + f"{firstnameEng}"
        password_account = generate_password()
        tel = input("Введите номер телефона: ")
        accounts = (login_ad_kos.lower(), login_ad_msk.lower(), password_account, fullName, firstnameRus, nameRus, lastnameRus, tel, firstnameEng, nameEng, lastnameEng)
        account.append(list(accounts))
    return create_account_ad(account)

# Создание паролей 
def generate_password():
    while True:
        alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
            return password

# Получение всех подразделений на домене
def get_ou(servers):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search(f'{servers[5]}', '(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=['ou'])
    else:
        conn.search(f'{servers[5]}', '(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=['ou'])
    all_ou = []
    for i,entry in enumerate(conn.entries, start=1):
        all_ou.append(entry.entry_dn)
        print(f"{i}. {entry.entry_dn}")
    conn.unbind()
    choice = int(input('В какое подразделение добавить пользователя введите номер подразделения: '))
    return all_ou[choice - 1]

# Получение всех Групп в домене
def add_group(servers, username):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search(f'{servers[5]}', '(objectClass=group)', attributes=ALL_ATTRIBUTES)
    else:
        conn.search(f'{servers[5]}', '(objectClass=group)', attributes=ALL_ATTRIBUTES)
    all_group = []
    for i,entry in enumerate(conn.entries, start=1):
        all_group.append(entry.entry_dn)
        print(f"{i}. {entry.cn}")
    choice = input('В какие группы добавить пользователя: ').split(' ')
    for index in choice:
        group = pyad.adgroup.ADGroup.from_dn(all_group[int(index) - 1])  # Поиск группы по имени
        group.add_members(username) 

# Получение полного пути пользователя в домене например "CN=zabbix,OU=ldap,OU=Пользователи,OU=USERS,DC=test,DC=local"
def get_user_path(servers, username):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search(f'{servers[5]}', f'(sAMAccountName={username[0]})')
    else:
        conn.search(f'{servers[5]}', f'(sAMAccountName={username[1]})')
    for entry in conn.entries:
        return entry.entry_dn

# Проверка логина пользователя в домене если есть совпадение логина то к логину нового пользователя добавляется одна буква например Иванов Иван Иванович -> ivanovii -> ivanovivi 
def check_account(servers, username):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search(f'{servers[5]}', '(objectClass=person)', attributes=ALL_ATTRIBUTES)
        for entry in conn.entries:
            login = entry['sAMAccountName'].value
            if username[0] == login:
                username[0] = f"{username[8].lower()}" + f"{username[9][0:2].lower()}" + f"{username[10][0].lower()}"
                break
    else:
        conn.search(f'{servers[5]}', '(objectClass=person)', attributes=ALL_ATTRIBUTES)
        for entry in conn.entries:
            login = entry['sAMAccountName'].value
            if username[1] == login:
                username[1] = f"{username[9][0:2].lower()}." + f"{username[8].lower()}"
                break 
    conn.unbind()
    return username

# Получение почт всех активированных пользователей если пользователь отключен то он игнорируется после получения почт происходит запись в csv файл. ВАЖНО в домене у пользователя поле mail b givenName должны быть заполнены.
def get_name_mail():
    server = Server(f'ldap://{servers[0][0]}')
    conn = Connection(server, user=f'{servers[0][1]}', password=f'{servers[0][2]}')
    conn.bind()
    conn.search(f'{servers[0][5]}','(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))', SUBTREE, attributes = ['displayName','mail'])
    with open('mail.csv', 'w', newline='', encoding="cp1251") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Имя', 'Почта'])

        for entry in conn.entries:
            displayName = entry.displayName
            mail = entry.mail
            if displayName != None and mail != None:
                csvwriter.writerow([displayName, mail])
    conn.unbind()

# Получение информации о пользователях в домене можно выполнить поиск по ФИО, по номеру телефона, либо получить информацию по всем пользователям введя all
def get_info_user():
    while True:
        tz = timedelta(hours=3)
        server = Server(f'{servers[0][0]}', get_info=ALL)
        conn = Connection(server, f'{servers[0][1]}', f'{servers[0][2]}', auto_bind=True)
        conn.search(f'{servers[0][5]}','(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))', SUBTREE, attributes =['cn','proxyAddresses','department','sAMAccountName', 'displayName', 'telephoneNumber', 'ipPhone', 'streetAddress','title','manager','objectGUID','company','lastLogon','mail','objectSid','memberOf','givenName'])
        name = list(conn.entries)
        userName = input('Введите ФИО, Фамилию или номер телефона пользователя \nдля вывода полного списка пользователеф введите all: ')
        if userName == 'all':
            for i in name:
                print(f'-----------------------------------------------------\nФИО: {i.cn}\nТелефон: {i.telephoneNumber}\nПочта: {i.mail}\nSSID: {i.objectSid}\nГруппы: {i.memberOf}\nЛогин: {i.sAMAccountName}\nАвторизация: {i.lastLogon.value+tz}\n------------------------------------------------------\n')
            conn.unbind()
            key = input('Для продолжения поиска пользователей нажмите "Y" для выхода из программы нажмите ENTER : ')
            if key == "y":
                continue
            else:
                break
        elif userName != 'all':
            userName = userName.split(',')
            for i in userName:
                for n in name:
                    if i.lstrip(' ').capitalize() == n.cn or i.lstrip(' ').capitalize() == n.givenName or i == n.telephoneNumber:
                        print(f'-----------------------------------------------------\nФИО: {n.cn}\nТелефон: {n.telephoneNumber}\nПочта: {n.mail}\nSSID: {n.objectSid}\nГруппы: {n.memberOf}\nЛогин: {n.sAMAccountName}\nАвторизация: {n.lastLogon.value+tz}\n------------------------------------------------------\n')
                        break
                continue
        conn.unbind()
        key = input('Для продолжения поиска пользователей нажмите "Y" для выхода из программы нажмите ENTER : ')
        if key == "y":
            continue
        else:
            break

# создание пользователя в домене и обновление его атррибутов
def create_account_ad(account):
    choice = int(input('На каком сервере создать аккаунт?\n1. AD-KOS\n2. AD-MSK\n3. На всех\n'))
    srv = []
    match choice:
        case 1:
            srv.append(servers[0])
        case 2:
            srv.append(servers[1])
        case 3:
            srv = servers
    info_account_kos = []
    info_account_msk = []
    info_server = []
    for server in srv:
        info_server.append(server)
        for user_account in account:
            check_account(server, user_account)
            ou = get_ou(server)
            pyad.set_defaults(ldap_server=server[0], username=server[1], password=server[2])
            new_user = pyad.aduser.ADUser.create(user_account[3], pyad.adcontainer.ADContainer.from_dn(ou))
            new_user.set_password(user_account[2])
            new_user.update_attribute('sn', f"{user_account[5]} {user_account[6]}")
            new_user.update_attribute('displayName', user_account[3])
            new_user.update_attribute('mail', f'{user_account[0]}@top-energo.com')
            new_user.update_attribute('telephoneNumber', user_account[7])
            new_user.update_attribute('givenName', user_account[4])
            if server[0] == '192.168.100.129':
                new_user.update_attribute('sAMAccountName', user_account[0])
                new_user.update_attribute('userPrincipalName', f"{user_account[0]}@{server[4]}")
                info_account_kos.append(user_account)
            else:
                new_user.update_attribute('sAMAccountName', user_account[1])
                new_user.update_attribute('userPrincipalName', f"{user_account[1]}@{server[4]}")
                info_account_msk.append(user_account)
            new_user.update_attribute("userAccountControl", 66080)
            add_group(server, new_user)
    for srv in info_server:
        if srv[0] == '192.168.100.129':   
            for login_kos in info_account_kos:
                print(f"{srv[3]}. top-energo\{login_kos[0]}: {login_kos[2]}")
        print('')
        if srv[0] == '192.168.100.128':
            for login_msk in info_account_msk:    
                print(f"{srv[3]}. top-energo\{login_msk[1]}: {login_msk[2]}")



choice = int(input('1) Создание Пользователя\n2) Выгрузка почт в csv\n3) Получение информации пользователей\n'))
servers = [('<ip-server-ad>', '<username-admin>', '<password>', 'AD-KOS', 'test-lan', 'dc=test,dc=lan'), ('<ip-server-ad>', '<username-admin>', '<password>', 'AD-MSK', 'test-local', 'dc=test,dc=local')]
match choice:
    case 1:
        username = generate_account(input('Введите ФИО пользователя: '))
    case 2:
        get_name_mail()
    case 3:
        get_info_user()



