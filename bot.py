#!/usr/bin/python
import asyncio
import subprocess
import os,stat
import telebot
from telebot import types
from telethon.sync import TelegramClient
import base64
import shutil
import datetime
import requests

# ВЕРСИЯ СКРИПТА 1.3
token='MyTokenFromBotFather' # ключ апи бота
usernames=[]
usernames.append('Mylogin') # Добавляем логины телеграма для администраторирования бота. Строчек может быть несколько
# следующие две строки заполняются с сайта https://my.telegram.org/apps
# вместо вас запрос будет посылать бот, оттуда и будут запрашиваться ключи
appapiid='myapiid'
appapihash='myiphash'

# следующие настройки могут быть оставлены по умолчанию, но можно будет что-то поменять
routerip='192.168.1.1' # ip роутера
dnsporttor='9153' # чтобы onion сайты открывался через любой браузер - любой открытый порт
localporttor='9141' # локальный порт для тор




# Начало работы программы

bot=telebot.TeleBot(token)
level=0
bypass=-1
sid="0"
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username not in usernames:
        bot.send_message(message.chat.id, 'Вы не являетесь автором канала')
        return
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Установка и удаление")
    item2 = types.KeyboardButton("Списки обхода")
    markup.add(item1,item2)
    bot.send_message(message.chat.id,'Добро пожаловать в меню!',reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    try:
        main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m1 = types.KeyboardButton("Установка и удаление")
        m2 = types.KeyboardButton("Списки обхода")
        main.add(m1, m2)
        if message.from_user.username not in usernames:
            bot.send_message(message.chat.id, 'Вы не являетесь автором канала')
            return
        if message.chat.type=='private':
            global level,bypass

            if (message.text == 'Назад'):
                bot.send_message(message.chat.id, 'Добро пожаловать в меню!', reply_markup=main)
                level=0
                bypass =-1
                return
            if level == 1:
                # значит это список обхода блокировок
                dirname = '/opt/etc/'
                dirfiles = os.listdir(dirname)

                for fln in dirfiles:
                    if fln == message.text+'.txt':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("Показать список")
                        item2 = types.KeyboardButton("Добавить в список")
                        item3 = types.KeyboardButton("Удалить из списка")
                        back = types.KeyboardButton("Назад")
                        markup.row(item1, item2, item3)
                        markup.row(back)
                        level = 2
                        bypass = message.text
                        bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                        return

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Назад")
                markup.add(back)
                bot.send_message(message.chat.id, "Не найден", reply_markup=markup)
                return

            if level==2 and message.text=="Показать список":
                f=open('/opt/etc/'+bypass+'.txt')
                flag=True
                s=''
                sites=[]
                for l in f:
                    sites.append(l)
                    flag=False
                if flag:
                    s='Список пуст'
                f.close()
                sites.sort()
                if not(flag):
                    for l in sites:
                        s=str(s)+'\n'+l.replace("\n","")

                bot.send_message(message.chat.id, s)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Показать список")
                item2 = types.KeyboardButton("Добавить в список")
                item3 = types.KeyboardButton("Удалить из списка")
                back = types.KeyboardButton("Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 2 and message.text == "Добавить в список":
                bot.send_message(message.chat.id,
                                 "Введите имя сайта или домена для разблокировки, либо воспользуйтесь меню для других действий")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Добавить обход блокировок соцсетей")
                back = types.KeyboardButton("Назад")
                markup.add(item1, back)
                level = 3
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 2 and message.text == "Удалить из списка":
                bot.send_message(message.chat.id,
                                 "Введите имя сайта или домена для удаления из листа разблокировки, либо возвратитесь в главное меню")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Назад")
                markup.add(back)
                level = 4
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 3:
                f = open('/opt/etc/' + bypass + '.txt')
                mylist = set()
                k = len(mylist)
                for l in f:
                    mylist.add(l.replace('\n', ''))
                f.close()
                if (message.text == "Добавить обход блокировок соцсетей"):
                    url = "https://raw.githubusercontent.com/sysadminatr/vivvaunblock/main/socialnet.txt"
                    s = requests.get(url).text
                    lst = s.split('\n')
                    for l in lst:
                        if len(l) > 1:
                            mylist.add(l.replace('\n', ''))
                else:
                    if len(message.text) > 1:
                        mas=message.text.split('\n')
                        for site in mas:
                            mylist.add(site)
                sortlist = []
                for l in mylist:
                    sortlist.append(l)
                sortlist.sort()
                f = open('/opt/etc/' + bypass + '.txt', 'w')
                for l in sortlist:
                    f.write(l + '\n')
                f.close()
                if (k != len(sortlist)):
                    bot.send_message(message.chat.id, "Успешно добавлено")
                else:
                    bot.send_message(message.chat.id, "Было добавлено ранее")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Показать список")
                item2 = types.KeyboardButton("Добавить в список")
                item3 = types.KeyboardButton("Удалить из списка")
                back = types.KeyboardButton("Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                subprocess.call(["/opt/bin/unblock_update.sh"])
                level = 2
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 4:
                f = open('/opt/etc/' + bypass + '.txt')
                mylist = set()
                k = len(mylist)
                for l in f:
                    mylist.add(l.replace('\n', ''))
                f.close()
                mas=message.text.split('\n')
                for site in mas:
                    mylist.discard(site)
                f = open('/opt/etc/' + bypass + '.txt', 'w')
                for l in mylist:
                    f.write(l + '\n')
                f.close()
                if (k != len(mylist)):
                    bot.send_message(message.chat.id, "Успешно удалено")
                else:
                    bot.send_message(message.chat.id, "Не найдено в списке")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Показать список")
                item2 = types.KeyboardButton("Добавить в список")
                item3 = types.KeyboardButton("Удалить из списка")
                back = types.KeyboardButton("Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                level = 2
                subprocess.call(["/opt/bin/unblock_update.sh"])
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return
            if level == 6:
                tormanually(message.text)
                subprocess.call(["/opt/etc/init.d/S35tor", "restart"])
                level=0
                bot.send_message(message.chat.id, 'Успешно обновлено', reply_markup=main)
                return
            if (message.text == 'Установка и удаление'):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Установка \ переустановка")
                item2 = types.KeyboardButton("Удаление")
                item3 = types.KeyboardButton("Переустановить ТОР")
                item5 = types.KeyboardButton("Переустановить ТОР вручную")

                back = types.KeyboardButton("Назад")
                markup.row(item1, item2)
                markup.row(item3, item4)
                markup.row(item5)
                markup.row(item6,item7)
                markup.row(back)
                bot.send_message(message.chat.id, 'Установка и удаление', reply_markup=markup)
                return
            if (message.text == 'Переустановить ТОР'):
                tor()
                subprocess.call(["/opt/etc/init.d/S35tor", "restart"])

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Установка \ переустановка")
                item2 = types.KeyboardButton("Удаление")
                item3 = types.KeyboardButton("Переустановить ТОР")
                item5 = types.KeyboardButton("Переустановить ТОР вручную")

                back = types.KeyboardButton("Назад")
                markup.row(item1, item2)
                markup.row(item3, item4)
                markup.row(item5)
                markup.row(item6,item7)
                markup.row(back)
                bot.send_message(message.chat.id, 'Установка и удаление', reply_markup=markup)
                return
            if (message.text == 'Переустановить ТОР вручную'):
                bot.send_message(message.chat.id,
                                 "Скопируйте мосты сюда. Каждая новая строка - новый мост. Мост должен начинаться с obfs4")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Назад")
                markup.add(back)
                level = 6
                bot.send_message(message.chat.id, "Меню", reply_markup=markup)
                return
            if (message.text == 'Установка \ переустановка'):
                bot.send_message(message.chat.id, "Начинаем установку");
                # создаём скрипт установки
                script = '#!/bin/sh'
                script += '\nopkg update'  # Обновим opkg
                # установим пакеты
                script += '\nopkg install mc tor tor-geoip bind-dig cron dnsmasq-full ipset iptables obfs4 dnscrypt-proxy2'
                script += '\nipset create test hash:net'
                script += '\nmkdir /opt/etc/'
                f = open('/opt/etc/install.sh', 'w')
                f.write(script)
                f.close()
                os.chmod('/opt/etc/install.sh', stat.S_IXUSR)
                subprocess.call(["/opt/etc/install.sh"])
                os.remove("/opt/etc/install.sh")
                bot.send_message(message.chat.id, "Установка пакетов завершена. Продолжаем установку");
                # файл для создания множеств для обхода блокировок
                f = open('/opt/etc/ndm/fs.d/100-ipset.sh', 'w')
                f.write('#!/bin/sh\n\
                [ "$1" != "start" ] && exit 0\n\
                ipset create unblock hash:net -exist\n\
                exit 0')
                f.close()
                os.chmod("/opt/etc/ndm/fs.d/100-ipset.sh", stat.S_IXUSR)

                f = open('/opt/bin/unblock_update.sh', 'w')
                f.write('#!/bin/sh\n\
                ipset flush unblock\n\
                /opt/bin/unblock_dnsmasq.sh\n\
                /opt/etc/init.d/S56dnsmasq restart\n\
                /opt/bin/unblock_ipset.sh &')
                f.close()
                os.chmod("/opt/bin/unblock_update.sh", stat.S_IXUSR)

                f = open('/opt/etc/init.d/S99unblock', 'w')
                f.write('#!/bin/sh\n\
                [ "$1" != "start" ] && exit 0\n\
                /opt/bin/unblock_ipset.sh\n\
                python /opt/etc/bot.py &')
                f.close()
                os.chmod("/opt/etc/init.d/S99unblock", stat.S_IXUSR)

                f = open('/opt/etc/crontab')
                lines = f.readlines()
                f.close()
                newline='00 06 * * * root /opt/bin/unblock_ipset.sh';
                f = open('/opt/etc/crontab', 'w')
                isnewline=True
                for l in lines:
                    if l.replace("\n","")==newline:
                        isnewline=False
                    f.write(l.replace("\n","") + '\n')
                if isnewline:
                    f.write(newline + '\n')
                f.close()
                subprocess.call(["/opt/bin/unblock_update.sh"])
                bot.send_message(message.chat.id, "Установили изначальные скрипты");

                # получение мостов tor
                tor()
                bot.send_message(message.chat.id, "Установили мосты tor");
                f = open("/opt/etc/unblock.txt", 'w')
                f.close()
                url = "https://raw.githubusercontent.com/tas-unn/bypass_keenetic/master/unblock_ipset.sh"
                s = requests.get(url).text
                s = s.replace("9153", dnsovertlsport)
                f = open("/opt/bin/unblock_ipset.sh", 'w')
                f.write(s)
                f.close()
                os.chmod('/opt/bin/unblock_ipset.sh', stat.S_IXUSR)

                url = "https://raw.githubusercontent.com/tas-unn/bypass_keenetic/master/unblock.dnsmasq"
                s = requests.get(url).text
                s = s.replace("9153", dnsovertlsport)
                f = open("/opt/bin/unblock_dnsmasq.sh", 'w')
                f.write(s)
                f.close()
                os.chmod('/opt/bin/unblock_dnsmasq.sh', stat.S_IXUSR)

                url = "https://raw.githubusercontent.com/tas-unn/bypass_keenetic/master/100-redirect.sh"
                s = requests.get(url).text
                s = s.replace("9141", localport).replace("192.168.1.1", routerip)
                f = open("/opt/etc/ndm/netfilter.d/100-redirect.sh", 'w')
                f.write(s)
                f.close()
                os.chmod('/opt/etc/ndm/netfilter.d/100-redirect.sh', stat.S_IXUSR)

                bot.send_message(message.chat.id, "Скачали 3 основных скрипта разблокировок");

                bot.send_message(message.chat.id, "Установка завершена. Теперь нужно немного доснастроить роутер и перейти к спискам для разблокировок",
                                 reply_markup=main)
                return
            if (message.text == 'Удаление'):
                os.remove('/opt/etc/ndm/fs.d/100-ipset.sh')
                os.remove('/opt/bin/unblock_update.sh')
                os.remove('/opt/etc/init.d/S99unblock')
                os.remove('/opt/bin/unblock_ipset.sh')
                os.remove('/opt/etc/ndm/netfilter.d/100-redirect.sh')
                os.remove('/opt/bin/unblock_dnsmasq.sh')
                shutil.rmtree('/opt/etc/')
                f = open('/opt/etc/crontab')
                lines = f.readlines()
                f.close()
                f = open('/opt/etc/crontab', 'w')
                for l in lines:
                    if l != '00 06 * * * root /opt/bin/unblock_ipset.sh':
                        f.write(l + '\n')
                f.close()
                script = '#!/bin/sh'
                script += '\nopkg update'  # Обновим opkg
                # установим пакеты
                script += '\nopkg remove  mc tor tor-geoip bind-dig cron dnsmasq-full ipset iptables obfs4 dnscrypt-proxy2'
                f = open('/opt/etc/remove.sh', 'w')
                f.write(script)
                f.close()
                os.chmod('/opt/etc/remove.sh', stat.S_IXUSR)
                subprocess.call(["/opt/etc/remove.sh"])
                os.remove("/opt/etc/remove.sh")
                bot.send_message(message.chat.id, 'Успешно удалено', reply_markup=main)
                return
            if (message.text == 'Добавление других подключений'):
                bot.send_message(message.chat.id, 'Когда-нибудь позже', reply_markup=main)
                return
            if (message.text == "Списки обхода"):
                level = 1
                dirname = '/opt/etc/'
                dirfiles = os.listdir(dirname)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for fln in dirfiles:
                    markup.add(fln.replace(".txt", ""))
                back = types.KeyboardButton("Назад")
                markup.add(back)
                bot.send_message(message.chat.id, "Списки обхода", reply_markup=markup)
                return
    except Exception as err:
        fl=open("/opt/etc/error.log","w")
        fl.write(str(err))
        fl.close()

def tormanually(bridges):
    global localport, dnsport
    f = open('/opt/etc/tor/torrc', 'w')
    f.write('User root\n\
PidFile /opt/var/run/tor.pid\n\
ExcludeExitNodes {RU},{UA},{AM},{KG},{BY}\n\
StrictNodes 1\n\
TransPort 192.168.1.1:' + localport + '\n\
ExitRelay 0\n\
ExitPolicy reject *:*\n\
ExitPolicy reject6 *:*\n\
GeoIPFile /opt/share/tor/geoip\n\
GeoIPv6File /opt/share/tor/geoip6\n\
DataDirectory /opt/var/lib/tor\n\
UseBridges 1\n\
ClientTransportPlugin obfs4 exec /opt/sbin/obfs4proxy managed\n' + bridges.replace("obfs4", "Bridge obfs4"))
    f.close()


def tor():
    global appapiid, appapihash
    global localport, dnsport
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    f = open('/opt/etc/tor/torrc', 'w')
    with TelegramClient('GetBridgesBot', appapiid, appapihash) as client:
        client.send_message('GetBridgesBot', '/bridges')
    with TelegramClient('GetBridgesBot', appapiid, appapihash) as client:
        for message1 in client.iter_messages('GetBridgesBot'):
            f.write('User root\n\
PidFile /opt/var/run/tor.pid\n\
ExcludeExitNodes {RU},{UA},{AM},{KG},{BY}\n\
StrictNodes 1\n\
TransPort 192.168.1.1:' + localporttor + '\n\
ExitRelay 0\n\
ExitPolicy reject *:*\n\
ExitPolicy reject6 *:*\n\
GeoIPFile /opt/share/tor/geoip\n\
GeoIPv6File /opt/share/tor/geoip6\n\
DataDirectory /opt/var/lib/tor\n\
UseBridges 1\n\
ClientTransportPlugin obfs4 exec /opt/sbin/obfs4proxy managed\n' + message1.text.replace("Your bridges:\n",
                                                                                         "").replace(
                "obfs4", "Bridge obfs4"))
            f.close()
            break

#bot.polling(none_stop=True)
try:
    bot.infinity_polling()
except Exception as err:
    fl=open("/opt/etc/error.log","w")
    fl.write(str(err))
    fl.close()
