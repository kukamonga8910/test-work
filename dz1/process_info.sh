#!/bin/bash

echo ""
echo -e "==> Process stats at $(date +'%Y-%d-%m_%H-%M-%S') <=="
echo "--------------------------------------------"
echo ""


echo -e "==> CPU usage <==\n"

ps -eo %cpu,pid,user,comm --sort=-%cpu | head -n 5

echo ""

echo -e "==> MEM usage <==\n"

# Тут мне помогли немного хотелось сделать красивенько и читаемо )))))

ps -eo size,pid,user,comm --sort=-%mem | awk '
NR==1 {
    print "SIZE\tPID\tUSER\tCOMMAND"
    next
} 
{
    mb = $1 / 1024
    if (mb >= 1024) {
        gb = mb / 1024
        printf "%.2f GB\t%d\t%s\t%s\n", gb, $2, $3, $4
    } else {
        printf "%.2f MB\t%d\t%s\t%s\n", mb, $2, $3, $4
    }
}' | column -t -s $'\t' | head -n 5
