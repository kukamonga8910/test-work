from googletrans import Translator
import string, secrets
from pyad import *
from ldap3 import Server, Connection, ALL_ATTRIBUTES, ALL, SUBTREE

def generate_account(username):
    account = []
    for i, names in enumerate(username.split(","), start=1):
        fullName = names.strip()
        firstnameRus, nameRus, lastnameRus = fullName.split()
        translator = Translator()
        EngFullName = translator.translate(fullName)
        firstnameEng, nameEng, lastnameEng = EngFullName.text.split()
        login_ad_kos = f"{firstnameEng}" + f"{nameEng[0]}" + f"{lastnameEng[0]}"
        login_ad_msk = f"{nameEng[0]}." + f"{firstnameEng}"
        
        for srv in servers:
            server = Server(f'ldap://{srv[0]}', get_info=ALL)
            conn = Connection(server, user=f'{srv[1]}', password=f'{srv[2]}')
            if not conn.bind():
                print('Не удалось установить подключение:', conn.result)
            if srv[0] == '192.168.100.129':
#                exit()
                conn.search('dc=test,dc=lan', '(objectClass=person)', attributes=ALL_ATTRIBUTES)
                for entry in conn.entries:
                    username = entry['sAMAccountName'].value
                    if username == login_ad_kos.lower():
                        login_ad_kos = f"{firstnameEng}" + f"{nameEng[0:2]}" + f"{lastnameEng[0]}"
                        break
            else:
                conn.search('dc=test,dc=local', '(objectClass=person)', attributes=ALL_ATTRIBUTES)
                for entry in conn.entries:
                    username = entry['sAMAccountName'].value
                    if username == login_ad_msk.lower():
                        login_ad_msk = f"{nameEng[0:2]}." + f"{firstnameEng}"
                        break
        conn.unbind()
        password_account = generate_password()
        tel = input("Введите номер телефона: ")
        accounts = (login_ad_kos.lower(), login_ad_msk.lower(), password_account, fullName, firstnameRus, nameRus, lastnameRus, tel, firstnameEng, nameEng, lastnameEng)
        account.append(list(accounts))
    for i, login in enumerate(account, start=1):
        print(f"{i}. top-energo\{login[0]}: {login[2]}; top-energo\{login[1]}: {login[2]}")

    return create_account_ad(account)
        
def generate_password():
    while True:
        alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
            return password
        
def get_ou(servers):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search('dc=test,dc=lan', '(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=['ou'])
    else:
        conn.search('dc=test,dc=local', '(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=['ou'])
    all_ou = []
    for i,entry in enumerate(conn.entries, start=1):
        all_ou.append(entry.entry_dn)
        print(f"{i}. {entry.ou}")
    conn.unbind()
    choice = int(input('В какое подразделение добавить пользователя введите номер подразделения: '))
    return all_ou[choice - 1]

def add_group(servers, username):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        conn.search('dc=test,dc=lan', '(objectClass=group)', attributes=ALL_ATTRIBUTES)
    else:
        conn.search('dc=test,dc=local', '(objectClass=group)', attributes=ALL_ATTRIBUTES)
    all_group = []
    for i,entry in enumerate(conn.entries, start=1):
        all_group.append(entry.entry_dn)
        print(f"{i}. {entry.cn}")
    choice = input('В какие группы добавить пользователя: ').split(' ')
    for index in choice:
        group = pyad.adgroup.ADGroup.from_dn(all_group[int(index) - 1])  # Поиск группы по имени
        group.add_members(username) 


def get_user_path(servers, username):
    server = Server(f'ldap://{servers[0]}', get_info=ALL)
    conn = Connection(server, user=f'{servers[1]}', password=f'{servers[2]}')
    conn.bind()
    if servers[0] == '192.168.100.129':
        search_base = 'dc=test,dc=lan'
        conn.search(search_base, f'(sAMAccountName={username[0]})')
    else:
        search_base = 'dc=test,dc=local'
        conn.search(search_base, f'(sAMAccountName={username[1]})')
    for entry in conn.entries:
        return entry.entry_dn

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
    for server in srv:
        for user_account in account:
            ou = get_ou(server)
            pyad.set_defaults(ldap_server=server[0], username=server[1], password=server[2])
            new_user = pyad.aduser.ADUser.create(user_account[3], pyad.adcontainer.ADContainer.from_dn(ou))
            new_user.set_password(user_account[2])
            new_user.update_attribute('sn', f"{user_account[5]} {user_account[6]}")
            new_user.update_attribute('displayName', user_account[3])
            new_user.update_attribute('mail', f'{user_account[0]}@top-energo.com')
            new_user.update_attribute('telephoneNumber', user_account[7])
            if server[0] == '192.168.100.129':
                new_user.update_attribute('sAMAccountName', user_account[0])
                new_user.update_attribute('userPrincipalName', user_account[0])
            else:
                new_user.update_attribute('sAMAccountName', user_account[1])
                new_user.update_attribute('userPrincipalName', user_account[1])
            new_user.update_attribute("userAccountControl", 66112)
            add_group(server, new_user)


servers = [('192.168.100.129', 'ldap', 'QAZqaz123'), ('192.168.100.128', 'ldap', 'QAZqaz123')]
username = generate_account(input('Введите ФИО пользователя: '))