#!/usr/bin/python3

import os, socket, subprocess as sp, smtplib
from email.mime.text import MIMEText


def ssl_checker():
    url = 'docs.top-energo.com'
    port = 443
    ip = socket.gethostbyname(url)
    date = sp.getoutput('date')
    ssl_check = sp.getoutput(f'echo | openssl s_client -servername {url} -connect {url}:{port} 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d "=" -f 2')
    now_epoch = sp.getoutput('date +%s')
    expire_epoch = sp.getoutput(f'date --date="{ssl_check}" "+%s"')
    expire_days = (int(expire_epoch) - int(now_epoch)) // (3600 * 24)
    return main(expire_days, ip, url, ssl_check, date)

def send_email(message):
    sender = "mail_account"
    # your password = "your password"
    password = "password"
    to_sender = "it@top-energo.com"
    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
#    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Проверка SSL сертификата docs.top-energo.com "
        server.sendmail(sender, to_sender, msg.as_string())

        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

def main(days, ip, url, ssl_check, date):
    if days == 89 or days == 90:
        os.system('> /home/ssl-check.log')
        with open('/home/ssl-check.log', 'a') as files:
            files.write("Сертификат Успешно обновлён\n" "Запуск скрипта - " f'{date}\n' "Домен - " f'{url}\n' "IP адрес домена - " f'{ip}\n' "Дата истечения сертификата - " f'{ssl_check}' " - " f"{days} days\n\n" )
        message = f"Сертификат успешно обновлен! До окончания работы сертификата осталось {days} days"
        print(send_email(message=message))

    elif days == 15:
        with open('/home/ssl-check.log', 'a') as files:
            files.write("Завтра в 07:00 будет обновлен сертификат\n" "Запуск скрипта - " f'{date}\n' "Домен - " f'{url}\n' "IP адрес домена - " f'{ip}\n' "Дата истечения сертификата - " f'{ssl_check}' " - " f"{days} days\n\n" )
        message = f"До истечения сертификата осталось {days} days!!! Завтра в 07:00 будет проведено обновление сертификата."
        print(send_email(message=message))
    elif days == 14:
        os.system("sed -i '/SSLEngine on/s/^/#/' /etc/httpd/conf.d/docs.top-energo.com.conf")
        os.system('systemctl restart httpd')
        os.system('certbot --force-renewal -d docs.top-energo.com')
        os.system("sed -i '/SSLEngine on/s/^#\+//' /etc/httpd/conf.d/docs.top-energo.com.conf")
        os.system('systemctl restart httpd')
        return ssl_checker()
    else:
        with open('/home/ssl-check.log', 'a') as files:
            files.write("Сертификат действителен\n" "Запуск скрипта - " f'{date}\n' "Домен - " f'{url}\n' "IP адрес домена - " f'{ip}\n' "Дата истечения сертификата - " f'{ssl_check}' " - " f"{days} days\n\n")

ssl_checker()
