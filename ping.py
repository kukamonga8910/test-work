from pythonping import ping
import datetime
import time
import os
import smtplib
from email.mime.text import MIMEText
sleep_interval = 120  # (In seconds) Check Interval
source = {'192.168.10.222': 'ECOSYS P3145dn'}

def stat_ip_logs(ping,ip_source,name_source): #resource availability check function #Logging function if ping is high
    if ping <= 500:
        show_res ='ONLINE'
    elif ping <= 1500:
         show_res ='FREZEE'
    else:
        show_res ='OFFLINE'
        error_logs = open("error_logs.txt", 'a')
        error_logs.write(cur_date_t+' | OFFLINE '+' | '+ip_source+' | '+name_source+"\n") #Write to file, date, status, ip source, name source
        error_logs.close()
        message = f'Дата: {cur_date_t}\nПринтер: {name_source}\nIP Адресс: {ip_source}\nPING: {ping}\nСтатус: {show_res}'
        mail(message=message)
    return show_res
    print(show_res)

def mail(message):
    sender = "cheker@top-energo.com"
    # your password = "your password"
    password = "y7Nq5yft4bgvvzLshved"
    to_sender = "it@top-energo.com"
    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
#    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Мониторинг принтера ECOSYS P3145dn"
        server.sendmail(sender, to_sender, msg.as_string())

        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

while True:
    now = datetime.datetime.now() #Current Date
    cur_date_t = now.strftime("%d.%m.%Y %H:%M %S") #Formatting the date output
    os.system('cls||clear') #Clear the console

    print('\n PINGg >-| Date:',cur_date_t,'| Check Interval:',sleep_interval,'sec.\n')
    print('\t|','Name      >  IP address             >  Ping  >\t Status')
    print('\t|');
    print('\t|--------------------------------------');
    print('\t|');
    for key, value in source.items():
        f_key, f_value = key, value
        if f_key and f_value: 
           rlw = ping (f_key, size= 30, count= 4).rtt_avg_ms
           print('\t|  %s    > %s            >' % (f_value,f_key),rlw,' >\t  ', stat_ip_logs(rlw,f_key,f_value))
           if rlw > 1500:
               exit() 
        f_key, f_value = key, value
    print('\t|');
    print('\t|--------------------------------------');
    print('\t|');
    print('\t| ',sleep_interval,'sec. - Интервал ожидания');
    print('\t| ',"ONLINE",' - ping меньше 500 msec.')
    print('\t| ',"FREZEE",' - ping больше 500 msec.')
    print('\t| ',"OFFLINE",'- ping больше 1500 ms.')
    print('\t|');
    print('\t|--------------------------------------\n');
    #Countdown timer
    for x in reversed(range(sleep_interval)):
       print('\r\t Refresh after:  '+str(sleep_interval - x),end=" sec.\r")
       time.sleep(1)
    continue