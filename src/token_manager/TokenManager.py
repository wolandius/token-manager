#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Copyright (c) 2017 Борис Макаренко
Copyright (c) 2020-2023 Владлен Мурылев

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения и сопутствующей документации
(в дальнейшем именуемыми «Программное Обеспечение»), безвозмездно использовать Программное Обеспечение без ограничений,
включая неограниченное право на использование, копирование, изменение, добавление, публикацию, распространение,
сублицензирование и/или продажу копий Программного Обеспечения, а также лицам, которым предоставляется данное
Программное Обеспечение, при соблюдении следующих условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во все копии или значимые части
данного Программного Обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ,
ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ
ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ
ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ
ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ..

Copyright (c) 2017 Boris Makarenko
Copyright (c) 2020-2023 Vladlen Murylev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import gettext
import os, gi, re, subprocess, platform, sys, webbrowser
import time, locale

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from datetime import datetime

VERSION = "5.2.3"

GUI_USERS = os.popen("w | grep -c xdm").readline().strip()
appdir = os.popen("echo $APPDIR").readline().strip()

APP='token_manager'
LOCALE_DIR=f"{appdir}/usr/share/locale/" if appdir else "/usr/share/locale/"
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext


builder = Gtk.Builder()
builder.set_translation_domain(APP)

# builder.add_from_file('../../data/ui/token_manager.glade')
builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/token_manager.glade') if appdir else builder.add_from_file('/usr/share/token_manager/ui/token_manager.glade')

if len(sys.argv) > 1:
    if sys.argv[1] == "--help":
        print("""Подсказки по использованию ключей в token-manager:
В данной реализации token-manager поддерживает явное указание архитектуры КриптоПро, вместо автоматического.
    --amd64         вызов 64-битной версии КриптоПро;
    --ia32          вызов 32-битной версии КриптоПро;
    --aarch64       вызов aarch64 версии КриптоПро;
    --e2k64         вызов e2k64 версии КриптоПро;
    --version       вывод номера версии token-manager;
    --debug-output  пробный вызов основных функций утилиты;
    --debug-output --amd64 пробный вызов основных функций утилиты для архитектуры amd64;
    --debug-output --ia32 пробный вызов основных функций утилиты для архитектуры ia32;
    --debug-output --aarch64 пробный вызов основных функций утилиты для архитектуры aarch64;
    --debug-output --e2k64 пробный вызов основных функций утилиты для архитектуры e2k64;""")
        exit(0)
    elif sys.argv[1] == "--amd64":
        arch = 'amd64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                '64-битная версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            # exit(-1)
    elif sys.argv[1] == "--ia32":
        arch = 'ia32'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                '32-битная версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            # exit(-1)
    elif sys.argv[1] == "--aarch64":
        arch = 'aarch64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                'aarch64 версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            # exit(-1)
    elif sys.argv[1] == "--e2k64":
        arch = 'e2k64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                'e2k64 версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            # exit(-1)
    elif sys.argv[1] == "--version":
        print(f"token-manager версия {VERSION}")
        exit(0)
    elif sys.argv[1] == "--debug-output":
        pass
    else:
        print("Ключ не опознан.")
        print("""Подсказки по использованию ключей в token-manager:
В данной реализации token-manager поддерживает явное указание архитектуры КриптоПро, вместо автоматического.
    --amd64         вызов 64-битной версии КриптоПро;
    --ia32          вызов 32-битной версии КриптоПро;
    --aarch64       вызов aarch64 версии КриптоПро;
    --e2k64         вызов e2k64 версии КриптоПро;
    --version       вывод номера версии token-manager;
    --debug-output  пробный вызов основных функций утилиты;
    --debug-output --amd64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --ia32 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --aarch64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --e2k64 пробный вызов основных функций утилиты для архитектуры e2k64;""")
        exit(-1)
else:
    if platform.machine() == 'x86_64':
        arch = 'amd64'
    elif platform.machine() == 'i686':
        arch = 'ia32'
    elif platform.machine() == 'aarch64':
        arch = 'aarch64'
    elif platform.machine() == 'e2k':
        arch = 'e2k64'
    else:
        exit(-1)

class Debug:
    def __init__(self):
        super(Debug, self).__init__()
        self.date = os.popen("echo $(date '+%F-%T')").readline().strip()
        self.name = f"/tmp/token-manager-{self.date}.txt"
        os.mknod(self.name)
        os.system(f'echo -e "\e[1;32mПроцесс начался, пожалуйста, дождитесь его завершения.\033[0m"')
        print()
        os.system(f"""echo -e "\e[1;31mВнимание!
Формируемый файл содержит конфиденциальную информацию с содержимым ваших сертификатов и хранилищ.
Просьба учитывать это при передаче файла.\033[0m" """)
        print()

    def show_crypto_version(self):
        os.system(f'echo -e "\e[1;32mВерсия КРИПТО ПРО\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        os.system(f"/opt/cprocsp/bin/{arch}/csptest -enum -info  >> {self.name}")
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')

    def whoami(self):
        os.system(f'echo -e "\e[1;32mWHOAMI\033[0m"  >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        os.system(f"echo $USERNAME >> {self.name}")
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')

    def check_funcs(self):
        os.system(f'echo -e "\e[1;32mИнформация для get_store_certs("uRoot")\033[0m"  >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        os.system(f"/opt/cprocsp/bin/{arch}/certmgr -list -store uRoot  >> {self.name}")
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        os.system(f'echo -e "\e[1;32mРезультат get_store_certs("uRoot")\033[0m"  >> {self.name}')
        for iter in get_store_certs("uRoot"):
            with open(self.name, 'a') as f:
                print(iter, file=f)
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        os.system(f'echo -e "\e[1;32mИнформация для get_store_certs("uMy")\033[0m"  >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name} ')
        os.system(f"/opt/cprocsp/bin/{arch}/certmgr -list -store uMy >> {self.name}")
        os.system(f'echo -e "\e[1;32mРезультат get_store_certs("uMy")\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m"  >> {self.name}')
        for iter in get_store_certs("uMy"):
            with open(self.name, 'a') as f:
                print(iter, file=f)
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32mИнформация для list_crls()\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m" >> {self.name}')
        os.system(f"/opt/cprocsp/bin/{arch}/certmgr -list -crl -store uRoot >> {self.name}")
        os.system(f'echo -e "\e[1;32mРезультат list_crls()\033[0m" >> {self.name}')
        for iter in list_crls():
            with open(self.name, 'a') as f:
                print(iter, file=f)
        os.system(f'echo -e "\e[1;32mИнформация для list_root_certs()\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m" >> {self.name}')
        os.system(f"/opt/cprocsp/bin/{arch}/certmgr -list -store uRoot >> {self.name}")
        os.system(f'echo -e "\e[1;32mРезультат list_root_certs()\033[0m" >> {self.name}')
        for iter in list_root_certs():
            with open(self.name, 'a') as f:
                print(iter, file=f)
        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m" >> {self.name}')
        os.system(f'echo -e "\e[1;32mРезультат get_token_certs(token[0])\033[0m" >> {self.name}')
        tokens = get_tokens()
        for i in range(1, len(tokens), 2):
            if tokens[i] != 1:
                with open(self.name, 'a') as f:
                    print(get_token_certs(tokens[i - 1][0]), file=f)
                stores = get_token_certs(tokens[i - 1][0])
                for j in range(1, len(stores), 2):
                    if stores[j] != 1:
                        os.system(f'echo -e "\e[1;32m---------------------------------\033[0m" >> {self.name}')
                        os.system(
                            f"""echo -e '\e[1;32mРезультат list_cert(stores[j-1][0].split("|")[1].strip())\033[0m'  >> {self.name}""")
                        with open(self.name, 'a') as f:
                            print(list_cert(stores[j - 1][0].split("|")[1].strip()), file=f)

        os.system(
            f"""echo -e "\e[1;32mСоздан файл \e[1;31m{self.name}\e[1;32m, для анализа файла просьба отправить его по адресу \e[1;31mredos.support@red-soft.ru\033[0m" """)
        os.system(
            f"""echo -e "\e[1;31mДанная информация не передается третьим лицам и используется исключительно для решения технических проблем.\033[0m" """)

from token_manager import token_pngs
# from . import token_pngs
# import token_pngs
root_png = token_pngs.root_png
personal_png = token_pngs.personal_png
usb_token_png = token_pngs.usb_token_png
def return_png(picture):
    pictures = {'root': root_png,
                'personal': personal_png,
                'usb': usb_token_png,
                }
    try:
        return pictures[picture]
    except KeyError:
        return None


def translate_cert_fields(fieldname):
    fields = {'1.2.840.113549.1.9.2': u'неструктурированное имя',
              '1.2.643.5.1.5.2.1.2': u'код должности',
              '1.2.643.5.1.5.2.1.1': u'код структурного подразделения ФССП России (ВКСП)',
              '1.2.643.5.1.5.2.2.1': u'Полномочия публикации обновлений ПО',
              '1.2.643.5.1.5.2.2.2': u'Подсистема АИС ФССП России',
              '1.2.643.5.1.24.2.9': u'Главный судебный пристав Российской Федерации',
              '1.2.643.5.1.24.2.10': u'Заместитель главного судебного пристава Российской Федерации',
              '1.2.643.5.1.24.2.11': u'Главный судебный пристав субъекта Российской Федерации',
              '1.2.643.5.1.24.2.12': u'Заместитель главного судебного пристава субъекта Российской Федерации',
              '1.2.643.5.1.24.2.13': u'Старший судебный пристав',
              '1.2.643.5.1.24.2.14': u'Судебный пристав-исполнитель',
              '1.2.643.100.2.1': u'Доступ к СМЭВ (ФЛ)',
              '1.2.643.100.2.2': u'Доступ к СМЭВ (ЮЛ)',
              '1.2.643.2.2.34.2': u'Временный доступ к Центру Регистрации',
              '1.2.643.2.2.34.4': u'Администратор Центра Регистрации КриптоПро УЦ',
              '1.2.643.2.2.34.5': u'Оператор Центра Регистрации КриптоПро УЦ',
              '1.2.643.2.2.34.6': u'Пользователь центра регистрации КриптоПро УЦ',
              '1.2.643.2.2.34.7': u'Центр Регистрации КриптоПро УЦ',
              '1.3.6.1.5.5.7.3.1': u'Проверка подлинности сервера',
              '1.3.6.1.5.5.7.3.2': u'Проверка подлинности клиента',
              '1.3.6.1.5.5.7.3.4': u'Защищенная электронная почта',
              '1.3.6.1.5.5.7.3.8': u'Установка штампа времени',
              '1.2.643.3.61.502710.1.6.3.4.1.1': u'Администратор организации',
              '1.2.643.3.61.502710.1.6.3.4.1.2': u'Уполномоченный специалист',
              '1.2.643.3.61.502710.1.6.3.4.1.3': u'Должностное лицо с правом подписи контракта',
              '1.2.643.3.61.502710.1.6.3.4.1.4': u'Специалист с правом направления проекта контракта участнику '
                                                 u'размещения заказа',
              '1.2.643.100.113.1': u'Класс средства ЭП КС 1',
              'CN': u'общее имя',
              'SN': u'фамилия',
              'G': u'имя и отчество',
              'I': u'инициалы',
              'T': u'должность',
              'OU': u'структурное подразделение',
              'O': u'организация',
              'L': u'населенный пункт',
              'S': u'субъект РФ',
              'C': u'страна',
              'E': u'адрес электронной почты',
              'INN': u'ИНН',
              'OGRN': u'ОГРН',
              'SNILS': u'СНИЛС',
              'STREET': 'название улицы, номер дома',
              'StreetAddress': u'адрес места нахождения',
              'Unstructured Name': 'неструктурированное имя'}
    try:
        return fields[fieldname]
    except KeyError:
        return fieldname


def get_cspversion():
    csptest = subprocess.Popen(['/opt/cprocsp/bin/%s/csptest' % arch, '-keyset', '-verifycontext'],
                               stdout=subprocess.PIPE)
    temp_output = csptest.communicate()[0].decode('utf-8')
    output = temp_output.split('\n')[0]
    r = re.search(r'v([0-9.]*[0-9]+)\ (.+)\ Release Ver\:([0-9.]*[0-9]+)\ OS\:([a-zA-z]+)', output)
    return r.group(1), r.group(2), r.group(3), r.group(4)


def check_user_pin():
    global appdir
    pkcs15tool = subprocess.Popen([f'{appdir}/usr/bin/pkcs15-tool', '-D'], stdout=subprocess.PIPE) if appdir else \
        subprocess.Popen(['/usr/bin/pkcs15-tool', '-D'], stdout=subprocess.PIPE)
    output = pkcs15tool.communicate()[0].decode("utf-8")
    search = 'User PIN'
    s = re.search(search, output)
    if s:
        auth_id = output.split('[User PIN]')[1].split('\n\t')[2].split(':')[-1].strip()
        return auth_id
    else:
        return None


def get_container_numeric_name(container):
    if versiontuple(get_cspversion()[2]) <= versiontuple("5.0.11455"):
        find_cont = os.popen(
            f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | iconv -f cp1251 | grep '{container}'").readlines()
    else:
        find_cont = os.popen(
            f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | grep '{container}'").readlines()
    return find_cont[0].split("|")[1].strip()


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def del_cont(cert):
    certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-delete', '-cont', cert], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output = certmgr.communicate()[0]
    if certmgr.returncode:
        return output
    return u"Сертификат успешно удален"


def del_store_cert(store, certID):
    certID = certID.strip()
    if store == 'uRoot':
        # try to find cert in mRoot at first
        certs = os.popen(f"/opt/cprocsp/bin/{arch}/certmgr -list -store mRoot | grep {certID}").readlines()
        if len(certs) > 0:
            # O = re.sub('"', '\\\"', O)
            # Cn = re.sub('"', '\\\"', Cn)
            certmgr = os.popen(
                f"""pkexec /opt/cprocsp/bin/{arch}/certmgr -delete -store mRoot -keyid "{certID}" """).readlines()
        else:
            certmgr = os.popen(
                f'echo 1 | /opt/cprocsp/bin/{arch}/certmgr -delete -store {store} -keyid "{certID}" ').readlines()
    else:
        certmgr = os.popen(
            f'echo 1 | /opt/cprocsp/bin/{arch}/certmgr -delete -store {store} -keyid "{certID}" ').readlines()
    var = ""
    if "[ErrorCode: 0x00000000]" in certmgr[-1]:
        return u"Сертификат успешно удален"
    else:
        for st in certmgr:
            var += st
        return var

def get_containers(is_hdimage):
    if versiontuple(get_cspversion()[2]) <= versiontuple("5.0.11455"):
        if is_hdimage:
            find_conts = os.popen(
                f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | iconv -f cp1251 | grep HDIMAGE").readlines()
        else:
            find_conts = os.popen(
                f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | iconv -f cp1251 | grep '\\\\'").readlines()
    else:
        if is_hdimage:
            find_conts = os.popen(
                f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | grep HDIMAGE").readlines()
        else:
            find_conts = os.popen(
                f"/opt/cprocsp/bin/{arch}/csptest -keyset -enum_cont -unique -fqcn -verifyc | grep '\\\\'").readlines()
    conts = []
    for cont in find_conts:
        cont = cont.split("|")[0].strip()
        conts.append(cont)
    return conts

def export_cert(container, path):
    output = os.popen(f"/opt/cprocsp/bin/amd64/certmgr -export -container '{container}' -dest '{path}'").readlines()
    for line in output:
        if "[ErrorCode: 0x00000000]" in line:
            return u"Сертификат успешно экспортирован"
    return output

def set_license(cpro_license):
    global appdir
    cpconfig = subprocess.Popen([f'{appdir}/usr/bin/cpconfig-%s' % arch, '-license', '-set', cpro_license],
                                stdout=subprocess.PIPE) if appdir else \
        subprocess.Popen(['/usr/bin/cpconfig-%s' % arch, '-license', '-set', cpro_license],
                                stdout=subprocess.PIPE)
    output = cpconfig.communicate()[0]
    if cpconfig.returncode:
        return output.split("\n")[-1], 1
    return None, 0

def install_root_cert(file, root):
    if root == "uRoot":
        certmgr = subprocess.Popen(
            ['/opt/cprocsp/bin/%s/certmgr' % arch, '-inst', '-store', f'{root}', '-file', file],
            stdout=subprocess.PIPE)
    elif root == "mRoot":
        certmgr = subprocess.Popen(
            [f'pkexec /opt/cprocsp/bin/{arch}/certmgr -inst -store {root} -file "{file}"'],
            stdout=subprocess.PIPE, shell=True)
    # output = certmgr.communicate()[0]

    output = certmgr.communicate()[0].decode("utf-8")
    m = []
    all_certs = create_certs_dict(output)
    counter = 1
    for single_cert in all_certs:
        single_cert_dict = create_single_cert_dict(all_certs[single_cert])
        cert_keys = list(single_cert_dict.keys())
        issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
        subjectKey = list(filter(lambda v: re.match(r'Subject|Субъект', v), cert_keys))
        SerialKey = list(filter(lambda v: re.match(r'Serial|Серийный номер', v), cert_keys))
        SHA1Key = list(filter(lambda v: re.match(r'SHA1 Hash|Хэш SHA1|SHA1 отпечаток', v), cert_keys))
        BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан', v), cert_keys))
        AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))

        issuerDN = create_dict_from_strk(single_cert_dict[issuerKey[0]])
        subjectDN = create_dict_from_strk(single_cert_dict[subjectKey[0]])

        # if
        part = (f"{counter}",
                issuerDN['CN'].strip() if "CN" in list(issuerDN.keys()) else issuerDN['O'].strip(),
                subjectDN['CN'].strip() if "CN" in list(subjectDN.keys()) else subjectDN['O'].strip(),
                single_cert_dict[SerialKey[0]].strip(),
                single_cert_dict[SHA1Key[0]].strip(),
                re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                )
        counter += 1
        m.append(part)
    return m

def install_crl(file, root):
    if root == "uRoot":
        certmgr = subprocess.Popen(
            ['/opt/cprocsp/bin/%s/certmgr' % arch, '-inst', '-crl', '-store', f'{root}', '-file', file],
            stdout=subprocess.PIPE)
    elif root == "mRoot":
        certmgr = subprocess.Popen(
            [f'pkexec /opt/cprocsp/bin/{arch}/certmgr -inst -crl -store {root} -file "{file}"'],
            stdout=subprocess.PIPE, shell=True)
    output = certmgr.communicate()[0].decode("utf-8")
    m = []
    all_certs = create_certs_dict(output)
    counter = 1
    for single_cert in all_certs:
        single_cert_dict = create_single_cert_dict(all_certs[single_cert])
        cert_keys = list(single_cert_dict.keys())
        issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
        BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан|Выпущен', v), cert_keys))
        AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))
        issuerDN = create_dict_from_strk(single_cert_dict[issuerKey[0]])
        part1 = [f"{counter}",
                 issuerDN['CN'].strip(),
                 re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                 re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                 ]
        m.append(part1)
    return m


def inst_cert_from_file(filepath, store):
    if store == "uMy":
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-inst', '-store', store, '-file',
                                    filepath], stdout=subprocess.PIPE)
    elif store == "mMy":
        certmgr = subprocess.Popen(['pkexec', '/opt/cprocsp/bin/%s/certmgr' % arch, '-inst', '-store', store, '-file',
                                    filepath], stdout=subprocess.PIPE)
    output = certmgr.communicate()[0]
    if certmgr.returncode:
        return output.split("\n")[-1]
    return u"Сертификат успешно установлен"

def get_UC_CDP(output):
    regex_string_CA = r'^URL сертификата УЦ.*?: http.*\.crt\n|' \
                      r'URL сертификата УЦ.*?: http.*\.cer|' \
                      r'^CA cert URL.*?: http.*\.crt\n|' \
                      r'URL сертификата УЦ.*?: http.*\.cer'
    regex_string_CDP = r'^URL списка отзыва.*?: http.*\.crl\n|' \
                       r'^CDP.*?: http.*\.crl\n'
    resub_string_CA = r'URL сертификата УЦ.*?: |' \
                      r'CA cert URL.*?: '
    resub_string_CDP = r'URL списка отзыва.*?: |' \
                       r'CDP.*?: '

    certs_UC_str = ""
    certs_UC = re.findall(regex_string_CA, output, re.MULTILINE + re.DOTALL)
    if len(certs_UC) > 0:
        certs_UC = certs_UC[0].strip().split("\n")
        for cert in certs_UC:
            if ".crt" in cert or ".cer" in cert:
                cert = re.sub(resub_string_CA, "", cert)
                certs_UC_str += cert + "\n"
    certs_UC_str = certs_UC_str[:-1]
    certs_CDP_str = ""
    certs_CDP = re.findall(regex_string_CDP, output, re.MULTILINE + re.DOTALL)
    if len(certs_CDP) > 0:
        certs_CDP = certs_CDP[0].strip().split("\n")
        for cert in certs_CDP:
            if ".crl" in cert:
                cert = re.sub(resub_string_CDP, "", cert)
                certs_CDP_str += cert + "\n"
    certs_CDP_str = certs_CDP_str[:-1]
    return [certs_UC_str, certs_CDP_str]

def get_cert_info_from_file(file):
    if versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9708"):
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-file', file],
                                   stdout=subprocess.PIPE)
    else:
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-verbose', '-file', file],
                                   stdout=subprocess.PIPE)
    output = certmgr.communicate()[0].decode('utf-8')
    lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
    m = []
    for i in range(1, len(lists), 2):
        certs_UC_str = ""
        certs_CDP_str = ""
        certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
        m.append(certs_UC_str)
        m.append(certs_CDP_str)
    return m

def get_store_certs(store):
    if store == 'uRoot':
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-store', 'uRoot'],
                                   stdout=subprocess.PIPE)
        output = certmgr.communicate()[0].decode("utf-8")
        m = []
        all_certs = create_certs_dict(output)
        counter = 1
        for single_cert in all_certs:
            single_cert_dict = create_single_cert_dict(all_certs[single_cert])
            cert_keys = list(single_cert_dict.keys())
            issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
            subjectKey = list(filter(lambda v: re.match(r'Subject|Субъект', v), cert_keys))
            SerialKey = list(filter(lambda v: re.match(r'Serial|Серийный номер', v), cert_keys))
            SHA1Key = list(filter(lambda v: re.match(r'SHA1 Hash|Хэш SHA1|SHA1 отпечаток', v), cert_keys))
            SubjKeyID = list(filter(lambda v: re.match(r'SubjKeyID|Идентификатор ключа', v), cert_keys))
            BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан', v), cert_keys))
            AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))
            part = (f"{counter}",
                    single_cert_dict[issuerKey[0]].strip(),
                    single_cert_dict[subjectKey[0]].strip(),
                    single_cert_dict[SerialKey[0]].strip(),
                    single_cert_dict[SHA1Key[0]].strip(),
                    single_cert_dict[SubjKeyID[0]].strip(),
                    re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                    re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                    )
            counter += 1
            m.append(part)
    else:
        if versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9708"):
            certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-store', store],
                                       stdout=subprocess.PIPE)
        else:
            certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-verbose', '-store', store],
                                       stdout=subprocess.PIPE)
        output = certmgr.communicate()[0].decode('utf-8')
        m = []
        all_certs = create_certs_dict(output)
        counter = 1
        for single_cert in all_certs:
            single_cert_dict = create_single_cert_dict(all_certs[single_cert])
            cert_keys = list(single_cert_dict.keys())
            issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
            subjectKey = list(filter(lambda v: re.match(r'Subject|Субъект', v), cert_keys))
            SerialKey = list(filter(lambda v: re.match(r'Serial|Серийный номер', v), cert_keys))
            SHA1Key = list(filter(lambda v: re.match(r'SHA1 Hash|Хэш SHA1|SHA1 отпечаток', v), cert_keys))
            SubjKeyID = list(filter(lambda v: re.match(r'SubjKeyID|Идентификатор ключа', v), cert_keys))
            BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан', v), cert_keys))
            AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))
            ExtendedKey = list(filter(lambda v: re.match(r'Назначение/EKU|Extended Key Usage', v), cert_keys))
            part1 = [f"{counter}",
                     single_cert_dict[issuerKey[0]].strip(),
                     single_cert_dict[subjectKey[0]].strip(),
                     single_cert_dict[SerialKey[0]].strip(),
                     single_cert_dict[SHA1Key[0]].strip(),
                     single_cert_dict[SubjKeyID[0]].strip(),
                     re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                     re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                     ]
            if ExtendedKey:
                part1.append(single_cert_dict[ExtendedKey[0]])
            certs_UC_str = ""
            certs_CDP_str = ""
            certs_UC_str, certs_CDP_str = get_UC_CDP(all_certs[single_cert])
            part1.append(certs_UC_str)
            part1.append(certs_CDP_str)
            m.append(part1)
            counter += 1
    return m

def install_CA_extra(url, root):
    name = url.split("/")[-1]
    os.system("mkdir -p /tmp/token-manager/CA")
    wget_out = subprocess.Popen(["wget", f"{url}",
                                 "-O", f"/tmp/token-manager/CA/{name}"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    output, error = wget_out.communicate()
    time.sleep(2)
    if wget_out.returncode != 0:
        print(error.decode("utf-8").strip())
        return [[url, error.decode("utf-8").strip()], 1]
    else:
        if root == "uRoot":
            install_root_cert(f"/tmp/token-manager/CA/{name}", "uRoot")
        elif root == "mRoot":
            install_root_cert(f"/tmp/token-manager/CA/{name}", "mRoot")
        return [url, 0]

def install_CDP_extra(url, root):
    name = url.split("/")[-1]
    os.system("mkdir -p /tmp/token-manager/CDP")
    wget_out = subprocess.Popen(["wget", f"{url}",
                                 "-O", f"/tmp/token-manager/CDP/{name}"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    output, error = wget_out.communicate()
    time.sleep(2)
    if wget_out.returncode != 0:
        print(error.decode("utf-8").strip())
        return [[url, error.decode("utf-8").strip()], 1]
    else:
        if root == "uRoot":
            install_crl(f"/tmp/token-manager/CDP/{name}", "uRoot")
        elif root == "mRoot":
            install_crl(f"/tmp/token-manager/CDP/{name}", "mRoot")
        return [url, 0]

def list_crls():
    certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-crl', '-store', 'uRoot'],
                               stdout=subprocess.PIPE)
    output = certmgr.communicate()[0].decode("utf-8")
    m = []
    all_certs = create_certs_dict(output)
    counter = 1
    for single_cert in all_certs:
        single_cert_dict = create_single_cert_dict(all_certs[single_cert])
        cert_keys = list(single_cert_dict.keys())
        issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
        BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан|Выпущен', v), cert_keys))
        AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))

        issuerDN = create_dict_from_strk(single_cert_dict[issuerKey[0]])

        part1 = [f"{counter}",
                 issuerDN['CN'].strip(),
                 re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                 re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                 ]
        m.append(part1)
    return m


def list_root_certs():
    certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-store', 'uRoot'],
                               stdout=subprocess.PIPE)
    output = certmgr.communicate()[0].decode("utf-8")
    m = []
    all_certs = create_certs_dict(output)
    counter = 1
    for single_cert in all_certs:
        single_cert_dict = create_single_cert_dict(all_certs[single_cert])
        cert_keys = list(single_cert_dict.keys())
        issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
        subjectKey = list(filter(lambda v: re.match(r'Subject|Субъект', v), cert_keys))
        SerialKey = list(filter(lambda v: re.match(r'Serial|Серийный номер', v), cert_keys))
        SHA1Key = list(filter(lambda v: re.match(r'SHA1 Hash|Хэш SHA1|SHA1 отпечаток', v), cert_keys))
        BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан', v), cert_keys))
        AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))

        issuerDN = create_dict_from_strk(single_cert_dict[issuerKey[0]])
        subjectDN = create_dict_from_strk(single_cert_dict[subjectKey[0]])

        part = (f"{counter}",
                issuerDN['CN'].strip() if "CN" in list(issuerDN.keys()) else issuerDN['O'].strip(),
                subjectDN['CN'].strip() if "CN" in list(subjectDN.keys()) else subjectDN['O'].strip(),
                single_cert_dict[SerialKey[0]].strip(),
                single_cert_dict[SHA1Key[0]].strip(),
                re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                )
        counter += 1
        m.append(part)
    return m


def get_first_part_certs():
    win = InfoClass()
    csptest = subprocess.Popen(['/opt/cprocsp/bin/%s/csptest' % arch, '-keyset', '-enum_cont', '-unique', '-fqcn',
                                '-verifyc'], stdout=subprocess.PIPE)
    try:
        if versiontuple(get_cspversion()[2]) <= versiontuple("5.0.11455"):
            output = csptest.communicate()[0].decode('cp1251').encode('utf-8').decode("utf-8")
            return [csptest, output]
        else:
            output = csptest.communicate()[0].decode("utf-8")
            return [csptest, output]
    except Exception as e:
        if int(GUI_USERS) == 0:
            print(f"Обнаружена неподдерживаемя кодировка  на токене.\n"
                  f"Поддерживаемые кодировки utf8 и cp1251\n"
                  f"Завершение работы программы\n\n"
                  f"{e}")
            exit(-1)
        elif int(GUI_USERS) >= 1:
            win.print_big_error(info=f"Обнаружена неподдерживаемя кодировка  на токене\n"
                                     f"Поддерживаемые кодировки utf8 и cp1251\n"
                                     f"Завершение работы программы\n\n"
                                     f"{e}", widtn=850, heigth=400)
            exit(-1)

def get_token_certs(token):
    csptest = get_first_part_certs()
    output = csptest[1]
    csptest = csptest[0]
    certs = []
    if csptest.returncode:
        return u'Ошибка', 1
    for line in output.split("\n"):
        if token in line:
            certs.append(line)
    return certs, 0


def get_ALL_certs():
    csptest = get_first_part_certs()
    output = csptest[1]
    csptest = csptest[0]
    certs = []
    if csptest.returncode:
        return u'Ошибка', 1
    for line in output.split("\n"):
        if "\\\\" in line:
            certs.append(line)
    return certs, 0


def get_tokens():
    list_pcsc = subprocess.Popen(['/opt/cprocsp/bin/%s/list_pcsc' % arch], stdout=subprocess.PIPE)
    output = list_pcsc.communicate()[0].decode('utf-8')
    if 'ERROR' in output:
        return u'<ключевых носителей не обнаружено>', 1
    m = re.findall(r'(?:available reader: |^)(.+)', output, re.MULTILINE)
    return m, 0


def list_cert(cert):
    if versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9708"):
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-cont', cert],
                                   stdout=subprocess.PIPE)
    else:
        certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-verbose', '-cont', cert],
                                   stdout=subprocess.PIPE)
    output = certmgr.communicate()[0].decode("utf-8")
    lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
    m = []
    counter = 1
    m = []
    all_certs = create_certs_dict(output)
    counter = 1
    for single_cert in all_certs:
        single_cert_dict = create_single_cert_dict(all_certs[single_cert])
        cert_keys = list(single_cert_dict.keys())
        issuerKey = list(filter(lambda v: re.match(r'Issuer|Издатель', v), cert_keys))
        subjectKey = list(filter(lambda v: re.match(r'Subject|Субъект', v), cert_keys))
        SerialKey = list(filter(lambda v: re.match(r'Serial|Серийный номер', v), cert_keys))
        SHA1Key = list(filter(lambda v: re.match(r'SHA1 Hash|Хэш SHA1|SHA1 отпечаток', v), cert_keys))
        SubjKeyID = list(filter(lambda v: re.match(r'SubjKeyID|Идентификатор ключа', v), cert_keys))
        BeforeKey = list(filter(lambda v: re.match(r'Not valid before|Выдан', v), cert_keys))
        AfterKey = list(filter(lambda v: re.match(r'Not valid after|Истекает', v), cert_keys))
        ExtendedKey = list(filter(lambda v: re.match(r'Назначение/EKU|Extended Key Usage', v), cert_keys))
        part1 = [f"{counter}",
                 single_cert_dict[issuerKey[0]].strip(),
                 single_cert_dict[subjectKey[0]].strip(),
                 single_cert_dict[SerialKey[0]].strip(),
                 single_cert_dict[SHA1Key[0]].strip(),
                 single_cert_dict[SubjKeyID[0]].strip(),
                 re.sub("UTC", "", single_cert_dict[BeforeKey[0]]).strip() + " ",
                 re.sub("UTC", "", single_cert_dict[AfterKey[0]]).strip() + " ",
                 ]
        if ExtendedKey:
            part1.append(single_cert_dict[ExtendedKey[0]])
        certs_UC_str = ""
        certs_CDP_str = ""
        certs_UC_str, certs_CDP_str = get_UC_CDP(all_certs[single_cert])
        part1.append(certs_UC_str)
        part1.append(certs_CDP_str)
        m.append(part1)
        counter += 1

    return m

def create_certs_dict(strk):
    strk_keys = re.findall(r"\d+-{7}\n", strk.strip(), re.MULTILINE + re.DOTALL)
    strk_list = re.split('\d+\-{7}\n', strk.strip())[1:]
    new_dict = {}
    counter_keys = 0
    for i in range(0, len(strk_list)):
        temp_str = strk_list[i].strip()
        new_dict[strk_keys[counter_keys]] = temp_str if i != len(strk_list) - 1 else re.split("==.*\n", temp_str)[0]
        counter_keys += 1
    return new_dict


def create_single_cert_dict(strk):
    if re.findall(r'(Назначение/EKU|Extended Key Usage)', strk.strip(), re.MULTILINE + re.DOTALL):
        parts = re.split(r'(Назначение/EKU|Extended Key Usage)', strk.strip(), re.MULTILINE + re.DOTALL)
        strk_keys1 = re.findall("^([A-Za-zА-Яа-я0-9 ]+?)\:", parts[0], re.MULTILINE + re.DOTALL)
        strk_rows = re.findall(r'^([A-Za-zА-Яа-я0-9 ]+?)\:(.+?)[\n].*?', parts[0], re.MULTILINE + re.DOTALL)
        keys_dict_count = {i[0].strip(): strk_keys1.count(i[0]) for i in strk_rows}
        new_dict = {}
        for k in keys_dict_count:
            new_dict[k] = [] if keys_dict_count[k] > 1 else ""
        for el in strk_rows:
            el0 = el[0].strip()
            if type(new_dict[el0]) is str:
                new_dict[el0] = el[1]
            elif type(new_dict[el0]) is list:
                new_dict[el0].append(el[1])
        strk_keys2 = parts[1]
        strk_rows2 = parts[2]
        strk_rows2 = re.sub(":", "", strk_rows2.strip()).split("\n")
        new_dict[strk_keys2] = []
        for k in strk_rows2:
            new_dict[strk_keys2].append(k.strip())
    else:
        strk_rows = re.findall(r'^([A-Za-zА-Яа-я0-9 ]+?)\:(.+?)[\n].*?', strk.strip(), re.MULTILINE + re.DOTALL)
        strk_keys = re.findall("^([A-Za-zА-Яа-я0-9 ]+?)\:", strk.strip(), re.MULTILINE + re.DOTALL)
        keys_dict_count = {i[0].strip(): strk_keys.count(i[0]) for i in strk_rows}
        new_dict = {}
        for k in keys_dict_count:
            new_dict[k] = [] if keys_dict_count[k] > 1 else ""
        for el in strk_rows:
            el0 = el[0].strip()
            if type(new_dict[el0]) is str:
                new_dict[el0] = el[1]
            elif type(new_dict[el0]) is list:
                new_dict[el0].append(el[1])
    return new_dict


def create_dict_from_strk(strk):
    strk_keys = re.findall("([A-Za-z0-9\.]+?)=", strk.strip())

    strk_list = re.split("([A-Za-z0-9\.]+?)=", strk.strip())[1:]
    new_dict = {}
    counter_keys = 0
    for i in range(1, len(strk_list), 2):
        temp_str = strk_list[i].strip()
        new_dict[strk_keys[counter_keys]] = temp_str[:-1] if "," == temp_str[-1] else temp_str
        counter_keys += 1
    return new_dict


if len(sys.argv) == 2 and sys.argv[1] == "--debug-output":
    if platform.machine() == 'x86_64':
        arch = 'amd64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                '64-битная версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            exit(-1)
    elif platform.machine() == 'i686':
        arch = 'ia32'
    elif platform.machine() == 'aarch64':
        arch = 'aarch64'
    elif platform.machine() == 'e2k':
        arch = 'e2k64'
    else:
        exit(-1)

    debug = Debug()
    debug.show_crypto_version()
    debug.check_funcs()
    exit(0)
elif len(sys.argv) == 3 and sys.argv[1] == "--debug-output":
    if sys.argv[2] == "--amd64":
        arch = 'amd64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                '64-битная версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            exit(-1)
    elif sys.argv[2] == "--ia32":
        arch = 'ia32'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                '32-битная версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            exit(-1)
    elif sys.argv[2] == "--aarch64":
        arch = 'aarch64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                'aarch64 версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            exit(-1)
    elif sys.argv[2] == "--e2k64":
        arch = 'e2k64'
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            print(
                'e2k64 версия СКЗИ Крипто Про CSP или некоторые его компоненты не установлены.\nЗавершение программы.')
            exit(-1)
    elif sys.argv[2] != "--amd64" and sys.argv[2] != "--ia32" and sys.argv[2] != "--aarch64" \
            and sys.argv[2] != "--e2k64":
        print("Ключ не опознан.")
        print("""Подсказки по использованию ключей в token-manager:
В данной реализации token-manager поддерживает явное указание архитектуры КриптоПро, вместо автоматического.
    --amd64         вызов 64-битной версии КриптоПро;
    --ia32          вызов 32-битной версии КриптоПро;
    --aarch64       вызов aarch64 версии КриптоПро;
    --e2k64         вызов e2k64 версии КриптоПро;
    --version       вывод номера версии token-manager;
    --debug-output  пробный вызов основных функций утилиты;
    --debug-output --amd64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --ia32 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --aarch64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --e2k64 пробный вызов основных функций утилиты для архитектуры e2k64;""")
        exit(-1)
    debug = Debug()
    debug.show_crypto_version()
    debug.check_funcs()
    exit(0)
elif len(sys.argv) > 2:
    print("Ключ не опознан.")
    print("""Подсказки по использованию ключей в token-manager:
В данной реализации token-manager поддерживает явное указание архитектуры КриптоПро, вместо автоматического.
    --amd64         вызов 64-битной версии КриптоПро;
    --ia32          вызов 32-битной версии КриптоПро;
    --aarch64       вызов aarch64 версии КриптоПро;
    --e2k64         вызов e2k64 версии КриптоПро;
    --version       вывод номера версии token-manager;
    --debug-output  пробный вызов основных функций утилиты;
    --debug-output --amd64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --ia32 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --aarch64 пробный вызов основных функций утилиты для архитектуры ;
    --debug-output --e2k64 пробный вызов основных функций утилиты для архитектуры e2k64;""")
    exit(-1)

class TokenUI:
    def __init__(self):
        self.window = builder.get_object("main_window")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            filename=f"{appdir}/usr/share/icons/hicolor/64x64/apps/token-manager.png"
        ) if appdir else GdkPixbuf.Pixbuf.new_from_file(
            filename="/usr/share/icons/hicolor/64x64/apps/token-manager.png"
        )

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.window.set_icon(image.get_pixbuf())

        self.info_class = InfoClass()
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            text = _("CIPF Crypto Pro CSP or some of its components are not installed for")
            self.info_class.print_simple_info(
                f'{text} {arch}.')
            exit(-1)
        text = _("The current version of CIPF Crypto Pro CSP is not supported.")
        if versiontuple("4.0.0") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.0"):
            if versiontuple(get_cspversion()[2]) < versiontuple("4.0.9708"):

                self.info_class.print_simple_info(text)
                exit(-1)
        elif versiontuple(get_cspversion()[2]) > versiontuple("5.0.0"):
            if versiontuple(get_cspversion()[2]) < versiontuple("5.0.11455"):
                self.info_class.print_simple_info(text)
                exit(-1)

        if not os.popen("systemctl list-unit-files | grep enabled | grep pcscd").readlines():
            os.system("systemctl enable --now pcscd")

        builder.get_object("add_license").connect("clicked", self.info_class.enter_license)
        builder.get_object("view_license").connect("clicked", self.view_license)

        builder.get_object("install_root_certs").connect("clicked", self.info_class.open_root_certs)
        builder.get_object("install_crl").connect("clicked", self.info_class.open_crl)
        builder.get_object("write_cert_to_cont").connect("clicked", self.write_cert)
        builder.get_object("export_cont_cert").connect("clicked", self.export_container_cert)
        builder.get_object("choose_local_cert_for_cont").connect("clicked", self.info_class.install_local_cert_to_container)
        builder.get_object("view_root").connect("clicked", self.view_root)
        builder.get_object("view_crl").connect("clicked", self.view_crl)

        builder.get_object("actionUsefull_install").connect("clicked", self.usefull_install)
        builder.get_object("actionUsefull_commands").connect("clicked", self.usefull_commands)

        builder.get_object("actionAbout").connect("clicked", self.about_window)

        builder.get_object("token_container").connect("clicked", self.token_container_install)
        builder.get_object("usb_flash_container").connect("clicked", self.usb_flash_container_install)
        builder.get_object("hdimage_container").connect("clicked", self.hdimage_container_install)

        self.token_refresh = builder.get_object("token_refresh")
        self.token_refresh.connect("clicked", self.refresh_token)

        self.token_list = Gtk.ListStore(str, str, str, bool)
        self.treeview = builder.get_object("token_treeview")
        self.treeview.set_model(self.token_list)
        self.treeview.get_selection().connect("changed", self.select_token)

        px_renderer = Gtk.CellRendererPixbuf()
        text = _("Select key media or vault")
        px_column = Gtk.TreeViewColumn(text)
        px_column.pack_start(px_renderer, False)
        str_renderer = Gtk.CellRendererText()
        px_column.pack_start(str_renderer, False)
        # set data connector function/method
        px_column.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        px_column.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        self.treeview.append_column(px_column)

        self.cachePIN = builder.get_object("cachePIN")
        self.cachePIN.set_sensitive(False)
        self.cachePIN.connect("clicked", self.cache_pin)

        self.changePIN = builder.get_object("changePIN")
        self.changePIN.set_sensitive(False)
        self.changePIN.connect("clicked", self.change_pin)

        # NEW model structure = {cert_index: type str, cert_item:, SubjKeyID: type str, color: type Gdk.RGBA}
        self.cert_list = Gtk.ListStore(str, str, str, Gdk.RGBA)
        self.treeview_cert = builder.get_object("treeview_cert")
        self.treeview_cert.set_model(self.cert_list)

        cell = Gtk.CellRendererText()
        text = _("Select certificate container")
        self.treeview_cert_col = Gtk.TreeViewColumn(text, cell, text=1, background_rgba=3)
        self.treeview_cert.append_column(self.treeview_cert_col)
        self.treeview_cert.get_selection().connect("changed", self.select_cert)

        self.cert_delete = builder.get_object("cert_delete")
        self.cert_delete.set_sensitive(False)
        self.cert_delete.connect("clicked", self.delete_cert)

        self.cert_view = builder.get_object("cert_view")
        self.cert_view.set_sensitive(False)

        self.handler_id_install = ""
        self.handler_id_view_cert = ""
        self.cert_install = builder.get_object("cert_install")
        self.cert_install.set_sensitive(False)

        self.token_refresh.clicked()
        self.window.show_all()

    ############################################################################################
    def about_window(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.add_from_file(
            f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file(
            '/usr/share/token_manager/ui/templates.glade')
        about = temp_builder.get_object("about_prog_window")
        pixbuf =  GdkPixbuf.Pixbuf.new_from_file(
            filename=f"{appdir}/usr/share/icons/hicolor/128x128/apps/token-manager.png"
        ) if appdir else GdkPixbuf.Pixbuf.new_from_file(
            filename="/usr/share/icons/hicolor/128x128/apps/token-manager.png"
        )
        about.set_logo(pixbuf)
        crypto_text = _("CryptoPRO version")
        temp_builder.get_object("about_crypto_label").set_text(f"{crypto_text}: {get_cspversion()[2]}")
        response = about.run()
        about.destroy()

    def select_token(self, selection):
        (model, iter) = selection.get_selected()
        self.cert_list.clear()
        if hasattr(self, 'cert_selection'):
            self.cert_selection.unselect_all()
        if model and iter:
            self.isToken = model.get_value(iter, 3)
            temp = model.get_value(iter, 2).split("||")
            self.store = temp[0]
            if self.isToken:  # isToken?
                self.cert_install.set_sensitive(True)
                self.token_name = model.get_value(iter, 1)
                if self.handler_id_install != "":
                    self.cert_install.disconnect(self.handler_id_install)
                self.handler_id_install = self.cert_install.connect("clicked", self.install_cert)
                text = _("Select certificate container")
                self.treeview_cert_col.set_title(text)
                # self.asReader.set_sensitive(True)
                self.token = temp[1]
                print(self.token)
                certs = get_token_certs(str(self.token))[0]
                counter = 0
                for cert in certs:
                    cert_item = cert.split('|')[0].split('\\')[-1]
                    self.cert_list.append([str(counter), cert_item, "", Gdk.RGBA(red=0, green=0, blue=0, alpha=0.1)])
                    counter+=1
            if not self.isToken:  # not isToken?
                self.cert_install.set_sensitive(True)
                if self.store == 'uRoot':
                    if self.handler_id_install != "":
                        self.cert_install.disconnect(self.handler_id_install)
                    self.handler_id_install = self.cert_install.connect("clicked", self.info_class.open_root_certs)
                elif self.store == 'uMy':
                    if self.handler_id_install != "":
                        self.cert_install.disconnect(self.handler_id_install)
                    # реализовать как в токене сбор данных и доустановку CA / CDP
                    self.handler_id_install = self.cert_install.connect("clicked", self.info_class.install_local_cert)
                # self.asReader.set_sensitive(False)
                self.changePIN.set_sensitive(False)
                self.cachePIN.set_sensitive(False)
                text = _("Select certificate")
                self.treeview_cert_col.set_title(text)
                certs = get_store_certs(model.get_value(iter, 2))
                for cert in certs:
                    self.cert_index = cert[0]
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=1)
                    if datetime.strptime(cert[6], '%d/%m/%Y  %H:%M:%S ') < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=0.1)
                    try:
                        cert_subject_cn = self.create_dict_from_strk(cert[2])
                        cert_subject_cn = cert_subject_cn['CN'] if 'CN' in cert_subject_cn else ""

                        cert_subject_o = self.create_dict_from_strk(cert[2])
                        cert_subject_o = cert_subject_o['O'] if 'O' in cert_subject_o else cert_subject_o['CN']

                        cert_issuer_cn = self.create_dict_from_strk(cert[2])
                        cert_issuer_cn = cert_issuer_cn['CN'] if 'CN' in cert_issuer_cn else ""

                        text1 = _("issued")
                        text2 = _("organization")
                        cert_item = "%s\n%s %s\n%s %s" % (cert_subject_cn, text1, cert_issuer_cn, text2, cert_subject_o)

                        cert_ID = cert[5]

                        self.cert_list.append([self.cert_index, cert_item, cert_ID, color, ])
                    except KeyError as e:
                        print(f" Couldn't parse {e}")
        return True

    def create_dict_from_strk(self, strk):
        strk_keys = re.findall("([A-Za-z0-9\.]+?)=", strk.strip())

        strk_list = re.split("([A-Za-z0-9\.]+?)=", strk.strip())[1:]
        new_dict = {}
        counter_keys = 0
        strk_list = strk_list[1::2]
        for i in range(0, len(strk_list)):
            temp_str = strk_list[i].strip()
            new_dict[strk_keys[counter_keys]] = temp_str[:-1] if "," == temp_str[-1] else temp_str
            counter_keys += 1
        return new_dict

    def write_cert(self, widget):
        win = InfoClass()

        containers = Gtk.ListStore(str, bool)
        if hasattr(self, 'tokens_for_import_container'):
            for token in self.tokens_for_import_container:
                temp_cont = get_token_certs(token[0])
                for cont in temp_cont:
                    if cont != 0:
                        for c in cont:
                            containers.append([c.split("|")[0].strip(), False])
            if len(containers) > 0:
                if win.install_container_from_token(containers):
                    selected_containers = win.return_liststore_containers()
                    name = ""
                    selected = 0
                    for cont in selected_containers:
                        if cont[1]:
                            selected += 1

                    if selected > 1:
                        text1 = _("Selected")
                        text2 = _("container(s),\nplease select only 1")
                        win.print_simple_info(f"{text1} {selected} {text2}")
                    elif selected == 1:
                        for cont in selected_containers:
                            if cont[1]:
                                container = rf"{cont[0]}"
                                container = re.sub(r'\\', r'\\\\', container)
                                container = re.sub(r'../..', r'\\.', container)
                                container = re.sub(r'\\\\\\', r'\\\\', container)
                                container = get_container_numeric_name(container)

                                output = win.install_new_cert_to_container(container)
                                flag_success = False
                                flag_cancel = False
                                text = _("Operation canceled by user")
                                if output == "success":
                                    flag_success = True
                                elif output == text:
                                    flag_cancel = True
                                if flag_success:
                                    text = _("The certificate was successfully copied to the container")
                                    win.print_simple_info(text)
                                elif flag_cancel:
                                    text = _("Operation canceled by user")
                                    win.print_simple_info(text)
                                else:
                                    win.print_big_error(output, 500, 300)
                else:
                    text = _("Operation canceled by user")
                    win.print_simple_info(text)
            else:
                text = _("Tokens not found")
                win.print_simple_info(text)
        else:
            text = _("Tokens not found")
            win.print_simple_info(text)

    def delete_cert(self, button):
        (model, iter) = self.cert_selection.get_selected()
        if self.isToken:
            if self.info_class.delete_from_Token() == Gtk.ResponseType.OK:
                ret = del_cont(self.cert)
                if ret == u"Сертификат успешно удален":
                    text = _("Certificate removed successfully")
                    self.info_class.print_simple_info(text)
                    self.cert_list.remove(iter)
                    self.cert_selection.unselect_all()
                else:
                    self.info_class.print_info(ret)

                self.cert_delete.set_sensitive(False)
                self.cert_view.set_sensitive(False)
                self.cert_install.set_sensitive(False)
        else:
            if self.info_class.delete_from_nonToken() == Gtk.ResponseType.OK:
                print(self.store, self.certID)
                ret = del_store_cert(self.store, self.certID)
                if ret == u"Сертификат успешно удален":
                    text = _("Certificate removed successfully")
                    self.info_class.print_simple_info(text)
                else:
                    self.info_class.print_info(ret, 1000, 500)
                self.cert_delete.set_sensitive(False)
                self.cert_view.set_sensitive(False)
                self.cert_install.set_sensitive(False)
                if ret == u"Сертификат успешно удален":
                    self.cert_list.remove(iter)
                    self.cert_selection.unselect_all()

    def select_cert(self, selection):
        self.cert_selection = selection
        (model, iter) = selection.get_selected()
        self.cert_model = model
        self.cert_model_iter = iter
        self.cert_install.set_sensitive(True)
        self.cert_view.set_sensitive(True)
        self.cert_delete.set_sensitive(True)
        self.cachePIN.set_sensitive(self.isToken)
        self.changePIN.set_sensitive(self.isToken)
        # self.asReader.set_sensitive(self.isToken)
        if self.handler_id_view_cert != "":
            self.cert_view.disconnect(self.handler_id_view_cert)
        if self.isToken:
            try:
                self.handler_id_view_cert = self.cert_view.connect("clicked", self.view_cert)
                containers = get_token_certs(self.token)
                cert_name = str(model.get_value(iter, 1))
                for line in containers[0]:
                    container = line

                    if cert_name.strip() in container.strip():
                        self.cert = line.split('|')[1]
                        self.cont_id = line.split('|')[1].split('\\')[
                                       4:]  # содержит список, который нужно объединить бэкслэшами
                        self.cont_name = line.split('|')[0].strip()
            except Exception as e:
                pass
        else:
            try:
                self.handler_id_view_cert = self.cert_view.connect("clicked", self.view_cert)
                self.certID = str(model.get_value(iter, 2))
            except Exception as e:
                pass

    def view_cert(self, widget):
        (model, iter) = self.cert_selection.get_selected()
        line = None
        if self.isToken:
            cert_info = list_cert(self.cert)
            if cert_info:
                line = cert_info[0]

        else:
            cert_info = get_store_certs(self.store)
            print(cert_info)
            cert_index = model.get_value(iter, 0)
            line = cert_info[int(cert_index) - 1]
            print(line)
        if line:
            cert_view = ViewCert()
            model = Gtk.ListStore(str, Gdk.RGBA)

            color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
            item = _("<b>Issuer</b>")
            model.append([item, color])
            issuer_info = dict(re.findall(
                '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)', line[1],
                re.UNICODE))
            for field in issuer_info:
                item = '<b>%s</b>: %s' % (translate_cert_fields(field), issuer_info[field])
                model.append([item, color])

            item = _('<b>Subject</b>:')
            model.append([item, color])
            subject_info = dict(re.findall(
                '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)', line[2],
                re.UNICODE))
            for field in subject_info:
                ""
                if subject_info[field][:2] == '"#':  # Если поле в HEX-виде
                    try:
                        item = ('<b>%s</b>: %s' % (
                            translate_cert_fields(field), subject_info[field][6:-1].decode('hex').decode('utf-8')))
                    except Exception as e:
                        item = ('<b>%s</b>: %s' % (
                            translate_cert_fields(field), subject_info[field][6:-1]))
                else:
                    item = ('<b>%s</b>: %s' % (translate_cert_fields(field), subject_info[field]))
                model.append([item, color])
            cert_serial = line[3][2:]
            text =_("Serial number")
            item = '<b>%s</b>: %s' % (text, cert_serial)
            model.append([item, color])
            not_valid_before = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
            text =  _("Not valid until")
            item = '<b>%s</b>: %s' % (text, datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S'))
            model.append([item, color])
            not_valid_after = datetime.strptime(line[7], '%d/%m/%Y  %H:%M:%S ')
            color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)  # transparent to apply system colors
            if not_valid_after < datetime.utcnow():
                color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
            text = _("Not valid after")
            item = '<b>%s</b>: %s' % (text, datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S'))
            model.append([item, color])
            item = _('<b>Advanced key usage</b>: ')
            model.append([item, color])
            try:
                if type(line[8]) == str:
                    lines = line[8].split('\n')
                    for i in range(0, len(lines)):
                        lines[i] = lines[i].strip()
                    ext_key = lines
                elif type(line[8]) == list:
                    ext_key = line[8]
            except IndexError:
                text = _("<i>Does not have</i>")
                ext_key = [text]
            for oid in ext_key:
                item = translate_cert_fields(oid)
                model.append([item, color])
            try:
                if type(line[9]) == str and len(line[9]) > 0:
                    item = _('<b>Required Root Certificates</b>: ')
                    model.append([item, color])
                    for l in line[9].split("\n"):
                        model.append([l, color])
                    self.CA_LIST_STR = line[9]
            except IndexError:
                pass
            try:
                if type(line[10]) == str and len(line[10]) > 0:
                    item = _('<b>Required CRLs</b>: ')
                    model.append([item, color])
                    for l in line[10].split("\n"):
                        model.append([l, color])
                    self.CDP_LIST_STR = line[10]
            except IndexError:
                pass
            text1 = _("View")
            text2 = _("Certificate")
            cert_view.viewcert_model(model, True, text1, text2)
        else:
            win = InfoClass()
            text = _("The public part of the certificate was not found")
            win.print_error(text)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        cell.set_property('text', model.get_value(iter, 1))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf',
                          GdkPixbuf.Pixbuf.new_from_data(
                              return_png(model.get_value(iter, 0)),
                              GdkPixbuf.Colorspace.RGB, True, 8,
                              20, 20, 80))

    def get_license(self):
        cpconfig = subprocess.Popen(['/opt/cprocsp/sbin/%s/cpconfig' % arch, '-license', '-view'],
                                    stdout=subprocess.PIPE)
        output = cpconfig.communicate()[0]
        return output

    def view_license(self, widget):
        license_info = self.get_license()
        license_view = ViewCert()
        item = license_info.decode("utf-8")
        item = item.split("\n")
        cert_listview = Gtk.ListStore(str)
        for it in item:
            cert_listview.append([it])
        title = _("View CryptoPRO CSP license")
        column = _("License")
        license_view.viewcert_model(model=cert_listview, with_color=False, title=title, column=column)

    def hdimage_container_install(self, widget):
        win = InfoClass()
        if win.install_HDIMAGE:
            containers = Gtk.ListStore(str, bool)
            conts = get_containers(is_hdimage=True)
            if len(conts) > 0:
                for cont in conts:
                    containers.append([cont, False])
                if win.install_container_from_hdimage(containers):
                    selected_containers_hdimage = win.return_liststore_hdimage_containers()
                    if len(selected_containers_hdimage) > 0:
                        selected_store_hdimage = None
                        selected_stores = 0
                        for cont in selected_containers_hdimage:
                            if cont[1]:
                                selected_store_hdimage = cont[0]
                                selected_stores += 1
                        if selected_stores == 1:
                            name = selected_store_hdimage.split("\\")
                            name = name[-1:][0]
                            out_name = win.enter_container_name(self, name)
                            if out_name != "empty" and out_name != "canceled":
                                container_name = out_name
                                dest_stores = get_tokens()[0]
                                text = _("<key carriers not found>")
                                if dest_stores != text:
                                    list_dest = Gtk.ListStore(str, bool)
                                    for store in dest_stores:
                                        list_dest.append([store, False])
                                    if win.choose_dest_stores(list_dest):
                                        selected_dest = win.return_liststore_dest_stores()
                                        selected_stores = 0
                                        for row in selected_dest:
                                            if row[1]:
                                                selected_store = row[0]
                                                selected_stores += 1
                                        if selected_stores > 1:
                                            text = _("You must select 1 storage\nto complete the export")
                                            win.print_error(text)
                                        elif selected_stores == 1:
                                            output = os.popen(
                                                f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{selected_store_hdimage}' "
                                                f"-contdest '\\\\.\\{selected_store}\\{container_name}'").readlines()

                                            if not win.install_cert_from_or_to_container(
                                                    f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                text = _("Operation canceled by user")
                                                win.print_simple_info(text)
                                    else:
                                        text = _("Operation canceled by user")
                                        win.print_simple_info(text)
                                else:
                                    text = _("Tokens not found")
                                    win.print_error(text)
                            elif out_name == "canceled":
                                text = _("Operation canceled by user")
                                win.print_simple_info(text)
                            elif out_name == "empty":
                                text = _("Name not entered")
                                win.print_error(text)
                        else:
                            text = _("Please choose only 1 container")
                            win.print_error(text)
                    else:
                        text = _("No containers selected")
                        win.print_error(text)
                else:
                    text = _("Operation canceled by user")
                    win.print_simple_info(text)
            else:
                text = _("No storage found in hdimage")
                win.print_error(text)

        else:
            text = _("Operation canceled by user")
            win.print_simple_info(text)

    def export_container_cert(self, widget):
        win = InfoClass()
        if win.install_HDIMAGE:
            containers = Gtk.ListStore(str, bool)
            conts = get_containers(is_hdimage=False)
            if len(conts) > 0:
                for cont in conts:
                    containers.append([cont, False])
                if win.select_container_to_import_cert(containers):
                    selected_containers = win.return_liststore_all_containers()
                    if len(selected_containers) > 0:
                        selected_store = None
                        selected_stores = 0
                        for cont in selected_containers:
                            if cont[1]:
                                selected_store = cont[0]
                                selected_stores += 1
                        if selected_stores == 1:
                            name = selected_store.split("\\")
                            name = name[-1:][0]
                            out_name = win.enter_cert_name(self, name)
                            if out_name != "empty" and out_name != "canceled":
                                cert_name = out_name
                                if "." in cert_name:
                                    cert_name = cert_name.split(".")[0]
                                path = win.choose_folder_dialog(self)
                                if path:
                                    output = export_cert(selected_store, f"{path}/{cert_name}.cer")
                                    if output == u"Сертификат успешно экспортирован":
                                        text = _("Certificate successfully exported")
                                        win.print_simple_info(text)
                                    else:
                                        win.print_big_error(output, 500, 300)
                                else:
                                    text = _("Operation canceled by user")
                                    win.print_simple_info(text)
                            elif out_name == "canceled":
                                text = _("Operation canceled by user")
                                win.print_simple_info(text)
                            elif out_name == "empty":
                                text = _("Name not entered")
                                win.print_error(text)
                        else:
                            text = _("Please choose only 1 container")
                            win.print_error(text)
                    else:
                        text = _("No containers selected")
                        win.print_error(text)
                else:
                    text = _("Operation canceled by user")
                    win.print_simple_info(text)
            else:
                text = _("Vaults not found")
                win.print_error(text)
        else:
            text = _("Operation canceled by user")
            win.print_simple_info(text)

    def token_container_install(self, widget):
        win = InfoClass()
        if win.install_HDIMAGE:
            containers = Gtk.ListStore(str, bool)
            if hasattr(self, 'tokens_for_import_container'):
                for token in self.tokens_for_import_container:
                    temp_cont = get_token_certs(token[0])
                    for cont in temp_cont:
                        if cont != 0:
                            for c in cont:
                                containers.append([c.split("|")[0].strip(), False])
                if len(containers) > 0:
                    if win.install_container_from_token(containers):
                        selected_containers = win.return_liststore_containers()
                        name = ""
                        selected = 0
                        for cont in selected_containers:
                            if cont[1]:
                                selected += 1
                        if selected > 1:
                            text1 = _("Selected")
                            text2 = _("container(s),\n"
                                      "prepare to enter passwords for containers\n"
                                      "several times and select certificates\n"
                                      "of the public part of the key\n"
                                      "(if they are not installed automatically")
                            win.print_simple_info(f"{text1} {selected} {text2}")
                        for cont in selected_containers:
                            if cont[1]:
                                name = cont[0].split("\\")
                                name = name[-1:][0]
                                out_name = win.enter_container_name(self, name)
                                if out_name != "empty" and out_name != "canceled":
                                    container_name = out_name
                                    dest_stores = get_tokens()[0]
                                    dest_stores.append("HDIMAGE")
                                    list_dest = Gtk.ListStore(str, bool)
                                    for store in dest_stores:
                                        list_dest.append([store, False])
                                    if win.choose_dest_stores(list_dest):
                                        selected_dest = win.return_liststore_dest_stores()
                                        selected_stores = 0
                                        for row in selected_dest:
                                            if row[1]:
                                                selected_store = row[0]
                                                selected_stores += 1
                                        if selected_stores != 1:
                                            text = _("You need to select 1 storage\nto complete the export")
                                            win.print_error(text)
                                        elif selected_stores == 1:
                                            output = os.popen(
                                                f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{cont[0]}' "
                                                f"-contdest '\\\\.\\{selected_store}\\{container_name}' | iconv -f cp1251").readlines()

                                            if not win.install_cert_from_or_to_container(
                                                    f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                text = _("Operation canceled by user")
                                                win.print_simple_info(text)
                                    else:
                                        text = _("Operation canceled by user")
                                        win.print_simple_info(text)
                                elif out_name == "canceled":
                                    text = _("Operation canceled by user")
                                    win.print_simple_info(text)
                                elif out_name == "empty":
                                    text = _("Name not entered")
                                    win.print_error(text)
                    else:
                        text = _("Operation canceled by user")
                        win.print_simple_info(text)
                else:
                    text = _("Tokens not found")
                    win.print_simple_info(text)
            else:
                text = _("Tokens not found")
                win.print_simple_info(text)
        else:
            text = _("Operation canceled by user")
            win.print_simple_info(text)

    def call_flash_container_install(self, secretnet):
        win = InfoClass()
        containers = Gtk.ListStore(str, bool)
        csptest = subprocess.Popen(
            ['/opt/cprocsp/bin/%s/csptest' % arch, '-keyset', '-enum_cont', '-unique', '-fqcn',
             '-verifyc'], stdout=subprocess.PIPE)
        output = csptest.communicate()[0].decode('cp1251').encode('utf-8').decode("utf-8")
        for line in output.split("\n"):
            if "FLASH" in line:
                containers.append([str(line).split("|")[0].strip(), False])
        if len(containers) > 0:
            if win.install_container_from_flash(containers):
                selected_containers = win.return_liststore_flashes()
                name = ""
                selected = 0
                for cont in selected_containers:
                    if cont[1]:
                        selected += 1
                        # path = win.choose_folder_container_dialog(self, secretnet)
                        # поиск имени по аналогии с флешками, в виду возможности наличия домена уровнем выше имени пользователя
                        domain_name = os.popen("echo $USERNAME").readlines()[0]
                        if "\\" in domain_name:
                            domain_name = domain_name.split("\\")[1]
                        elif "@" in domain_name:
                            domain_name = domain_name.split("@")[0]
                        find_name = os.popen(f"find /var/opt/cprocsp/keys/ -name {domain_name}").readlines()
                        if find_name:
                            find_name = find_name[0].strip()
                            if selected > 1:
                                text1 = _("Selected")
                                text2 = _("container(s),\n"
                                          "prepare to enter passwords for containers\n"
                                          "several times and select certificates\n"
                                          "of the public part of the key\n"
                                          "(if they are not installed automatically")
                                win.print_simple_info(f"{text1} {len(selected_containers)} {text2}")
                            for cont in selected_containers:
                                if cont[1]:
                                    name = cont[0].split("\\")
                                    name = name[-1:][0]
                                    out_name = win.enter_container_name(self, name)
                                    if out_name != "empty" and out_name != "canceled":
                                        container_name = out_name
                                        dest_stores = get_tokens()[0]
                                        if type(dest_stores) == list:
                                            dest_stores.append("HDIMAGE")
                                        elif type(dest_stores) == str and dest_stores == '<ключевых носителей не обнаружено>':
                                            dest_stores = ["HDIMAGE"]
                                        list_dest = Gtk.ListStore(str, bool)
                                        for store in dest_stores:
                                            list_dest.append([store, False])
                                        if win.choose_dest_stores(list_dest):
                                            selected_dest = win.return_liststore_dest_stores()
                                            selected_stores = 0
                                            for row in selected_dest:
                                                if row[1]:
                                                    selected_store = row[0]
                                                    selected_stores += 1
                                            if selected_stores != 1:
                                                text = _("You need to select 1 storage\nto complete the export")
                                                win.print_error(text)
                                            elif selected_stores == 1:
                                                output = os.popen(
                                                    f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{cont[0]}' "
                                                    f"-contdest '\\\\.\\{selected_store}\\{container_name}' | iconv -f cp1251").readlines()

                                                if not win.install_cert_from_or_to_container(
                                                        f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                    text = _("Operation canceled by user")
                                                    win.print_simple_info(text)
                                        else:
                                            text = _("Operation canceled by user")
                                            win.print_simple_info(text)
                                    elif out_name == "canceled":
                                        text = _("Operation canceled by user")
                                        win.print_simple_info(text)
                                    elif out_name == "empty":
                                        text = _("Name not entered")
                                        win.print_error(text)
                                else:
                                    text = _("Wrong path selected, operation canceled")
                                    win.print_simple_info(text)
            else:
                text = _("Operation canceled by user")
                win.print_simple_info(text)
        else:
            text = _("No containers found related to the usb-flash drive")
            win.print_simple_info(text)

    def usb_flash_container_install(self, widget):
        win = InfoClass()
        if win.install_HDIMAGE:
            # задаем пользователю явно указать контейнер, который определила крипта,
            # затем запрашиваем его физическое расположение и проверяем тем самым, верно ли был указан путь?

            find_secretnet = os.popen("rpm -qa | grep secretnet").readlines()
            if find_secretnet:
                status = win.call_secretnet_configs(self)
                if status == "installed":
                    self.call_flash_container_install(True)
                elif status == "just_installed":
                    text = _("Reconnect the usb-flash drive\nand repeat the operation")
                    win.print_simple_info(text)
                elif status == "canceled":
                    text = _("Operation canceled by user")
                    win.print_simple_info(text)
            else:
                self.call_flash_container_install(False)
        else:
            text = _("Operation canceled by user")
            win.print_simple_info(text)

    def install_cert(self, widget):
        win = InfoClass()
        ###
        # Проверка на наличие домена, если он есть, то включаем правило для secretnet
        # правило единое для всех доменных пользователей
        ###
        global appdir
        domain_info = os.popen(f"{appdir}/usr/sbin/realm list").readlines() if appdir else os.popen("/usr/sbin/realm list").readlines()
        if domain_info:
            text1 = _("domain users")
            status = self.info_class.call_secretnet_configs(text1, "domain")
            if status == "installed":

                if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.0"):
                    if win.ask_about_mmy(self) == Gtk.ResponseType.OK:
                        store = "mMy"
                    else:
                        store = "uMy"
                else:
                    store = "uMy"
                ret = self.inst_cert(self.cert, store)
                if ret == u"Сертификат успешно установлен":
                    cert_info = list_cert(self.cert)
                    line = cert_info[0]
                    CA_LIST_STR = ""
                    CDP_LIST_STR = ""
                    try:
                        if type(line[9]) == str and len(line[9]) > 0:
                            CA_LIST_STR = line[9]
                        if type(line[10]) == str and len(line[10]) > 0:
                            CDP_LIST_STR = line[10]
                    except IndexError:
                        pass
                    if CA_LIST_STR != "" or CDP_LIST_STR != "":
                        if win.ask_about_extras(self) == Gtk.ResponseType.OK:
                            strk_out = ""
                            errors_ca = []
                            success_ca = []
                            errors_cdp = []
                            success_cdp = []
                            if CA_LIST_STR != "":
                                for ca in CA_LIST_STR.split("\n"):
                                    out = install_CA_extra(ca, "mRoot") if store == "mMy" else install_CA_extra(ca, "uRoot")
                                    success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                    time.sleep(2)
                            if CDP_LIST_STR != "":
                                if CA_LIST_STR != "":
                                    strk_out += "\n"

                                for cdp in CDP_LIST_STR.split("\n"):
                                    out = install_CDP_extra(cdp, "mRoot") if store == "mMy" else install_CDP_extra(cdp, "uRoot")
                                    success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                    time.sleep(2)
                            if len(success_ca) > 0:
                                text = _("Successfully installed root certificates:")
                                strk_out.append(text)
                                for succ in success_ca:
                                    strk_out.append(f"{succ}")

                            if len(success_cdp) > 0:
                                if len(success_ca) > 0:
                                    strk_out += "\n"
                                text = _("Successfully installed CRLs:")
                                strk_out.append(text)
                                for succ in success_cdp:
                                    strk_out.append(f"{succ}")

                            if len(errors_ca) > 0:
                                if len(success_ca) > 0 or len(success_cdp) > 0:
                                    strk_out += "\n"
                                text = _("Error installing root certificates:")
                                strk_out.append(text)
                                for err in errors_ca:
                                    strk_out.append(f"{err[0]}\n{err[1]}")

                            if len(errors_cdp) > 0:
                                text = _("Error installing CRLs:")
                                strk_out.append(text)
                                for err in errors_cdp:
                                    strk_out.append(f"{err[0]}\n{err[1]}")
                            view = ViewCertOutput()
                            view.viewcertoutput_model(strk_out, "", "")
                        os.system("rm -rf /tmp/token-manager/")
                else:
                    # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
                    output = win.choose_open_cert_to_close_container(self.cert)
                    if not output[0]:
                        strk = ""
                        for line in output[1]:
                            strk += line
                        self.info_class.print_error(strk)
            elif status == "just_installed":
                text = _("Reconnect the usb-flash drive\nand repeat the operation")
                win.print_simple_info(text)
            elif status == "canceled":
                text = _("Operation canceled by user")
                win.print_simple_info(text)
        else:
            if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.0"):
                if win.ask_about_mmy(self) == Gtk.ResponseType.OK:
                    store = "mMy"
                else:
                    store = "uMy"
            else:
                store = "uMy"
            ret = self.inst_cert(self.cert, store)
            if ret == u"Сертификат успешно установлен":
                # self.info_class.print_simple_info(ret)
                cert_info = list_cert(self.cert)
                line = cert_info[0]
                CA_LIST_STR = ""
                CDP_LIST_STR = ""
                try:
                    if type(line[9]) == str and len(line[9]) > 0:
                        CA_LIST_STR = line[9]
                    if type(line[10]) == str and len(line[10]) > 0:
                        CDP_LIST_STR = line[10]
                except IndexError:
                    pass
                if CA_LIST_STR != "" or CDP_LIST_STR != "":
                    if win.ask_about_extras(self) == Gtk.ResponseType.OK:
                        strk_out = []
                        errors_ca = []
                        success_ca = []
                        errors_cdp = []
                        success_cdp = []
                        if CA_LIST_STR != "":

                            for ca in CA_LIST_STR.split("\n"):
                                out = install_CA_extra(ca, "mRoot") if store == "mMy" else install_CA_extra(ca, "uRoot")
                                success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                time.sleep(2)
                        if CDP_LIST_STR != "":
                            if CA_LIST_STR != "":
                                strk_out += "\n"
                            for cdp in CDP_LIST_STR.split("\n"):
                                out = install_CDP_extra(cdp, "mRoot") if store == "mMy" else install_CDP_extra(cdp, "uRoot")
                                success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                time.sleep(2)
                        if len(success_ca) > 0:
                            text = _("Successfully installed root certificates:")
                            strk_out.append(text)
                            for succ in success_ca:
                                strk_out.append(f"{succ}")

                        if len(success_cdp) > 0:
                            text = _("Successfully installed CRLs:")
                            strk_out.append(text)
                            for succ in success_cdp:
                                strk_out.append(f"{succ}")

                        if len(errors_ca) > 0:
                            text = _("Error installing root certificates:")
                            strk_out.append(text)
                            for err in errors_ca:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        if len(errors_cdp) > 0:
                            text = _("Error installing CRLs:")
                            strk_out.append(text)
                            for err in errors_cdp:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        view = ViewCertOutput()
                        view.viewcertoutput_model(strk_out, "", "")
                    os.system("rm -rf /tmp/token-manager/")
                else:
                    text = _("Certificate installed successfully")
                    self.info_class.print_simple_info(text)
            else:
                # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
                output = win.choose_open_cert_to_close_container(self.cert)
                if not output[0]:
                    strk = ""
                    for line in output[1]:
                        strk += line
                    self.info_class.print_error(strk)

    def inst_cert(self, cert, store):
        if store == "uMy":
            certmgr = os.popen(f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -cont '{cert}'").readlines()
        elif store == "mMy":
            certmgr = os.popen(f"pkexec /opt/cprocsp/bin/{arch}/certmgr -inst -store mMy -cont '{cert}'").readlines()
        for line in certmgr:
            if "[ErrorCode: 0x00000000]" in line:
                return u"Сертификат успешно установлен"
        return certmgr

    def view_root(self, widget):
        root_info = list_root_certs()
        root_view = ListCert()
        text = _("Root certificates")
        root_view.listcert_model(Gtk.ListStore(str, str, str, Gdk.RGBA), True, text, root_info, True)

    def view_crl(self, widget):
        crl_info = list_crls()
        crl_view = ListCert()
        text = _("CRLs")
        crl_view.listcert_model(Gtk.ListStore(str, str, Gdk.RGBA), True, text, crl_info, False)

    def usefull_install(self, widget):
        webbrowser.open_new_tab("https://redos.red-soft.ru/base/other-soft/szi/cryptopro/")

    def usefull_commands(self, widget):
        webbrowser.open_new_tab("https://redos.red-soft.ru/base/other-soft/szi/cryptopro/certs-cryptopro/")

    def refresh_token(self, button):
        self.token_list.clear()
        if hasattr(self, 'cert_selection'):
            self.cert_selection.unselect_all()
        tokens = get_tokens()
        root_store_item = TokenListItem()
        root_store_item.text = _("Root certificates storage")
        root_store_item.isToken = False
        root_store_item.storage = 'uRoot'
        root_store_item.icon = 'root'
        self.token_list.append(
            [root_store_item.icon, root_store_item.text, root_store_item.storage, root_store_item.isToken])

        personal_store_item = TokenListItem()
        personal_store_item.text = _("Personal certificates storage")
        personal_store_item.isToken = False
        personal_store_item.storage = 'uMy'
        personal_store_item.icon = "personal"
        self.token_list.append([personal_store_item.icon, personal_store_item.text, personal_store_item.storage,
                                personal_store_item.isToken])
        if tokens[1]:
            self.token_item = TokenListItem()
            self.token_item.text = _('<No Key Carriers Found>')
        else:
            self.tokens_for_import_container = Gtk.ListStore(str, bool)
            for token in tokens[0]:
                token_item = TokenListItem()
                token_item.token_name = token
                text = _("serial")
                token_item.text = ('%s - %s № %s' % (token, text, self.get_token_serial(token)))
                token_item.icon = "usb"
                self.token_list.append([token_item.icon, token_item.text, token_item.storage + "||" +
                                        token_item.token_name, token_item.isToken])
                self.tokens_for_import_container.append([token, False])

    def get_token_serial(self, token):
        global appdir
        opensc_tool = subprocess.Popen([f'{appdir}/usr/bin/opensc-tool', '--serial', '-r', token], stdout=subprocess.PIPE) if appdir else \
            subprocess.Popen(['/usr/bin/opensc-tool', '--serial', '-r', token], stdout=subprocess.PIPE)
        output = opensc_tool.communicate()[0]
        try:
            serial = str(int(''.join(output.decode('utf-8').split(' ')[:-1]), 16))
            if len(serial) < 10:
                while (len(serial) < 10):
                    serial = "0" + str(serial)
        except:
            return u'б/н'
        if not opensc_tool.returncode:
            return serial

    def versiontuple(self, v):
        return tuple(map(int, (v.split("."))))


    def set_as_reader(self, token):
        global appdir
        cpconfig = subprocess.Popen([f'{appdir}/usr/bin/cpconfig-%s' % arch, '-hardware', 'reader', '-add', f"{token}"],
                                    stdout=subprocess.PIPE) if appdir else \
        subprocess.Popen(['/usr/bin/cpconfig-%s' % arch, '-hardware', 'reader', '-add', f"{token}"],
                         stdout=subprocess.PIPE)
        output = cpconfig.communicate()[0].decode('utf-8')
        if "Succeeded, code:0x0" in output:
            return True
        else:
            return False

    def change_pin(self, button):
        container = f"\\\\.\\{self.token}\\{self.cont_id[0]}\\{self.cont_id[1]}\\{self.cont_id[2]}\\{self.cont_id[3]}"
        result = os.popen(f"/opt/cprocsp/bin/{arch}/csptest -passwd -qchange -container '{container}'").readlines()
        for line in result:
            if "[ErrorCode: 0x00000000]" in line:
                text = _("PIN code changed successfully")
                self.info_class.print_simple_info(text)

    def cache_pin(self, button):
        result = self.info_class.cache_pin()
        if (result[0] == Gtk.ResponseType.OK) and (result[1] != ''):
            if not self.add_ini(result[1], self.cont_id):
                text = _("PIN code saved successfully")
                self.info_class.print_simple_info(text)

    def add_ini(self, pin, cont_id):
        cpconfig = subprocess.Popen(['/opt/cprocsp/sbin/%s/cpconfig' % arch, '-ini',
                                     '\\LOCAL\\KeyDevices\\passwords\\%s\%s\%s' % tuple(cont_id[:-1]), '-add', 'string',
                                     'passwd', pin], stdout=subprocess.PIPE)
        return cpconfig.returncode


class TokenListItem:
    isToken = True
    storage = ''
    token_name = ''
    text = ''
    icon = ''

    def __init__(self):
        super(TokenListItem, self).__init__()

class ListCert(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

    def listcert_model(self, model, with_color, title, certlist_data, is_root):
        self.list_data = certlist_data
        self.is_root = is_root
        self.token_list = model
        self.filter = self.token_list.filter_new()
        self.filter.set_visible_func(self.visible_cb)

        temp_builder = Gtk.Builder()
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.set_translation_domain('token_manager')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')
        dialog = temp_builder.get_object("listcert_model")
        dialog.set_title(title)
        self.view = temp_builder.get_object("listcert_model_treeview")

        self.view.set_model(self.filter)
        cell = Gtk.CellRendererText()

        self.entry = temp_builder.get_object("listcert_model_entry")
        text = _("Type to filter...")
        self.entry.set_placeholder_text(text)
        self.entry.connect("changed", self.refresh_filter)

        if self.is_root:
            dialog.set_size_request(1300, 500)
            col1_text = _("Issuer")
            col1 = Gtk.TreeViewColumn(col1_text, cell, text=0, background_rgba=3)
            col2_text = _("Subject")
            col2 = Gtk.TreeViewColumn(col2_text, cell, text=1, background_rgba=3)
            col3_text = _("Basic information")
            col3 = Gtk.TreeViewColumn(col3_text, cell, text=2, background_rgba=3)

            self.view.append_column(col1)
            self.view.append_column(col2)
            self.view.append_column(col3)

            for line in self.list_data:
                not_valid_before = datetime.strptime(line[5], '%d/%m/%Y  %H:%M:%S ')
                not_valid_after = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
                color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                if not_valid_after < datetime.utcnow():
                    color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                text1 = _("Serial number")
                text3 = _("Not available until")
                text4 = _("Not available after")
                date1 = datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S')
                date2 = datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S')
                if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
                    text2 = _("SHA1 fingerprint")

                    item = (f"{text1}: {line[3]}\n{text2}: {line[4]}\n{text3}: {date1}\n{text4}: {date2}")
                else:
                    text2 = _("SHA1 hash")
                    item = (f"{text1}: {line[3]}\n{text2}: {line[4]}\n{text3}: {date1}\n{text4}: {date2}")
                self.token_list.append([line[1], line[2], item, color])
        else:
            self.set_default_size(800, 343)
            text1 = _("Subject")
            col1 = Gtk.TreeViewColumn(text1, cell, text=0, background_rgba=2)
            text2 = _("Dates")
            col2 = Gtk.TreeViewColumn(text2, cell, text=1, background_rgba=2)

            self.view.append_column(col1)
            self.view.append_column(col2)

            for line in self.list_data:
                this_update = datetime.strptime(line[2], '%d/%m/%Y  %H:%M:%S ')
                next_update = datetime.strptime(line[3], '%d/%m/%Y  %H:%M:%S ')
                color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)

                if next_update < datetime.utcnow():
                    color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                date1 = datetime.strftime(this_update, '%d.%m.%Y %H:%M:%S')
                date2 = datetime.strftime(next_update, '%d.%m.%Y %H:%M:%S')
                text1 = _("Date of issue")
                text2 = _("Update date")
                item = (f'{text1}: {date1} UTC\n{text2}: {date2} UTC')
                self.token_list.append([line[1], item, color])

        response = dialog.run()
        dialog.destroy()

    def refresh_filter(self, widget):
        self.filter.refilter()

    def visible_cb(self, model, iter, data=None):
        search_query = self.entry.get_text().lower()
        if search_query == "":
            return True
        value = model.get_value(iter, 0).lower()
        if value.startswith(search_query):
            return True
        return False
        value = model.get_value(iter, 0).lower()
        return True if value.startswith(search_query) else False


class ViewCert(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
    def viewcert_model(self, model, with_color, title, column):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')

        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("viewcert_model")
        dialog.set_title(title)
        self.view = temp_builder.get_object("viewcert_treeview")
        cell = Gtk.CellRendererText()
        if with_color:
            col = Gtk.TreeViewColumn(column, cell, markup=0, background_rgba=1)
        else:
            col = Gtk.TreeViewColumn(column, cell, markup=0)
        cell.set_property("editable", True)
        self.view.append_column(col)
        self.view.set_model(model)
        response = dialog.run()
        dialog.destroy()

class ViewCertOutput(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

    def viewcertoutput_model(self, info, title, column):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("viewcertoutput_model")
        dialog.set_title(title)
        self.view = temp_builder.get_object("viewcertoutput_model_treeview")
        self.liststore = Gtk.ListStore(str)
        for i in info:
            self.liststore.append([i])

        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        column_text = Gtk.TreeViewColumn(column, renderer_text, text=0)
        self.view.append_column(column_text)
        self.view.set_model(model=self.liststore)
        response = dialog.run()
        dialog.destroy()

class InfoClass(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

    def print_info(self, info, widtn, heigth):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        self.liststore = Gtk.ListStore(str)
        self.liststore.append([info])
        dialogWindow = temp_builder.get_object("print_info_window")
        treeview = temp_builder.get_object("print_info_treeview")
        treeview.set_model(self.liststore)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("", renderer_text, text=0)
        treeview.append_column(column_text)

        dialogWindow.set_size_request(widtn, heigth)
        response = dialogWindow.run()
        dialogWindow.destroy()

    def print_big_error(self, info, widtn, heigth):
        self.liststore = Gtk.ListStore(str)
        self.liststore.append([info])
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("print_big_error")
        dialogWindow.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("print_big_error_treeview")
        treeview.set_model(model=self.liststore)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("", renderer_text, text=0)
        treeview.append_column(column_text)
        dialogWindow.set_size_request(widtn, heigth)
        response = dialogWindow.run()
        dialogWindow.destroy()

    def print_simple_info(self, info):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("print_simple_info")
        dialog.props.text = info
        dialog.run()
        dialog.destroy()

    def print_error(self, error):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("print_error")
        dialog.props.text = error
        dialog.run()
        dialog.destroy()

    def cache_pin(self):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("cache_pin")
        pinEntry = temp_builder.get_object("pinEntry")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        response = dialogWindow.run()
        pin = pinEntry.get_text()
        dialogWindow.destroy()
        return [response, pin]

    def install_local_cert(self, widget):
        text = _("Choose file(s)")
        dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        text = _("Certificates")
        filter.set_name(f"{text} *.cer")
        filter.add_mime_type(text)
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.0"):
                if self.ask_about_mmy(self) == Gtk.ResponseType.OK:
                    store = "mMy"
                else:
                    store = "uMy"
            else:
                store = "uMy"
            ret = inst_cert_from_file(file_name, store)
            if ret == u"Сертификат успешно установлен":
                info = get_cert_info_from_file(file_name)
                CA_LIST_STR = ""
                CDP_LIST_STR = ""
                try:
                    if type(info[0]) == str and len(info[0]) > 0:
                        CA_LIST_STR = info[0]
                    if type(info[1]) == str and len(info[1]) > 0:
                        CDP_LIST_STR = info[1]
                except IndexError:
                    pass
                if CA_LIST_STR != "" or CDP_LIST_STR != "":
                    if self.ask_about_extras(self) == Gtk.ResponseType.OK:
                        strk_out = []
                        errors_ca = []
                        success_ca = []
                        errors_cdp = []
                        success_cdp = []
                        if CA_LIST_STR != "":
                            for ca in CA_LIST_STR.split("\n"):
                                out = install_CA_extra(ca, "mRoot") if store == "mMy" else install_CA_extra(ca, "uRoot")
                                success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                time.sleep(2)
                        if CDP_LIST_STR != "":
                            for cdp in CDP_LIST_STR.split("\n"):
                                out = install_CDP_extra(cdp, "mRoot") if store == "mMy" else install_CDP_extra(cdp, "uRoot")
                                success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                time.sleep(2)
                        if len(success_ca) > 0:
                            text = _("Successfully installed root certificates:")
                            strk_out.append(text)
                            for succ in success_ca:
                                strk_out.append(f"{succ}")

                        if len(success_cdp) > 0:
                            text = _("Successfully installed CRLs:")
                            strk_out.append(text)
                            for succ in success_cdp:
                                strk_out.append(f"{succ}")

                        if len(errors_ca) > 0:
                            text = _("Error installing root certificates:")
                            strk_out.append(text)
                            for err in errors_ca:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        if len(errors_cdp) > 0:
                            text = _("Error installing CRLs:")
                            strk_out.append(text)
                            for err in errors_cdp:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        view = ViewCertOutput()
                        view.viewcertoutput_model(strk_out, "", "")
                    os.system("rm -rf /tmp/token-manager/")
            else:
                self.print_info(ret, 350, 300)
        else:
            dialog.destroy()

    def enter_license(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("enter_license")
        userEntry = temp_builder.get_object("userEntry")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        response = dialogWindow.run()
        cpro_license = userEntry.get_text()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.OK) and (cpro_license != ''):
            l = set_license(cpro_license)
            if l[1]:
                text = _("An error has occurred")
                self.print_error(f'{text}: {l[0]}')
            else:
                text = _("License key successfully installed")
                self.print_simple_info(text)

    def enter_container_name(self, widget, old_name):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("enter_container_name")
        nameEntry = temp_builder.get_object("nameEntry")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        nameEntry.set_text(f"{old_name}_copy")
        dialogWindow.show_all()
        response = dialogWindow.run()
        container_name = nameEntry.get_text()
        dialogWindow.destroy()
        if response == Gtk.ResponseType.OK:
            if container_name != '':
                return container_name
            else:
                return "empty"
        elif response == Gtk.ResponseType.CANCEL:
            return "canceled"

    def enter_cert_name(self, widget, old_name):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("enter_cert_name")
        nameEntry = temp_builder.get_object("nameCertEntry")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        nameEntry.set_text(f"{old_name}_cert")
        response = dialogWindow.run()
        cert_name = nameEntry.get_text()
        dialogWindow.destroy()
        if response == Gtk.ResponseType.OK:
            if cert_name != '':
                return cert_name
            else:
                return "empty"
        elif response == Gtk.ResponseType.CANCEL:
            return "canceled"

    def open_root_certs(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("open_root_certs")
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_names = dialog.get_filenames()
            dialog.destroy()
            if self.ask_about_root(self) == Gtk.ResponseType.OK:
                root = "mRoot"
            else:
                root = "uRoot"
            if not file_names:
                return
            for file in file_names:
                root_view = ViewCert()
                model = Gtk.ListStore(str, Gdk.RGBA)
                root_info = install_root_cert(file, root)

                for line in root_info:
                    not_valid_before = datetime.strptime(line[5], '%d/%m/%Y  %H:%M:%S ')
                    not_valid_after = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                    if not_valid_after < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)

                    text1 = _("Issuer")
                    text2 = _("Subject")
                    text3 = _("Serial number")
                    text5 = _("Not valid until")
                    text6 = _("Not valid after")
                    date1 = datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S')
                    date2 = datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S')
                    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
                        text4 = _("SHA1 Fingerprint")
                        item = f'{text1}: {line[1]}\n' \
                               f'{text2}: {line[2]}\n' \
                               f'{text3}: {line[3]}\n' \
                               f'{text4}: {line[4]}\n' \
                               f'{text5}: {date1}\n' \
                               f'{text6}: {date2}'
                    else:
                        text4 = _("SHA1 hash")
                        item = f'{text1}: {line[1]}\n' \
                               f'{text2}: {line[2]}\n' \
                               f'{text3}: {line[3]}\n' \
                               f'{text4}: {line[4]}\n' \
                               f'{text5}: {date1}\n' \
                               f'{text6}: {date2}'
                    for it in item.split("\n"):
                        model.append([it, color])
                text1 = _("Root certificate installed")
                text2 = _("Certificate")
                root_view.viewcert_model(model, True, text1, text2)
        else:
            dialog.destroy()

    def delete_from_nonToken(self):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("delete_from_nonToken")
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def delete_from_Token(self):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("delete_from_Token")
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def open_crl(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialog = temp_builder.get_object("open_crl")
        dialog.set_size_request(800, 800)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if self.ask_about_root(self) == Gtk.ResponseType.OK:
                root = "mRoot"
            else:
                root = "uRoot"
            file_names = dialog.get_filenames()
            dialog.destroy()
            if not file_names:
                return
            crl_view = ViewCert()
            model = Gtk.ListStore(str, Gdk.RGBA)
            for filename in file_names:
                crl_info = install_crl(filename, root)
                for line in crl_info:
                    item = ""
                    this_update = datetime.strptime(line[2], '%d/%m/%Y  %H:%M:%S ')
                    next_update = datetime.strptime(line[3], '%d/%m/%Y  %H:%M:%S ')
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                    if next_update < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                    date1 = datetime.strftime(this_update, '%d.%m.%Y %H:%M:%S')
                    date2 = datetime.strftime(next_update, '%d.%m.%Y %H:%M:%S')
                    text1 = _("Date of issue")
                    text2 = _("Update date")
                    item = (f"{line[1]}\n{text1}: {date1} UTC\n{text2}: {date2} UTC")
                    model.append([item, color])
            text1 = _("CRLs installed")
            text2 = _("Certificate")
            crl_view.viewcert_model(model, True, text1, text2)
        else:
            dialog.destroy()

    def ask_about_root(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("ask_about_root")
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def ask_about_mmy(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("ask_about_mmy")
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def ask_about_extras(self, widget):
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("ask_about_extra_certs")
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def install_HDIMAGE(self, widget):
        find_hdimage = os.popen(f"/opt/cprocsp/sbin/{arch}/cpconfig -hardware reader -view | grep HDIMAGE").readlines()
        if not find_hdimage[0]:
            temp_builder = Gtk.Builder()
            temp_builder.set_translation_domain('token_manager')
            # temp_builder.add_from_file('../../data/ui/templates.glade')
            temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

            dialogWindow = temp_builder.get_object("install_HDIMAGE")
            pinEntry = temp_builder.get_object("pinEntry")
            pinEntry.set_visibility(False)
            response = dialogWindow.run()
            if response == Gtk.ResponseType.OK:
                pin = pinEntry.get_text()
                ROOTPSW = pin  # сделать окно диалог с запросом рут пароля. указать что будет создано хранилище
                output = os.popen(
                    f'su - root -c "/opt/cprocsp/sbin/{arch}/cpconfig -hardware reader -add HDIMAGE store" '
                    f'<<< "{ROOTPSW}"').readlines()
                dialogWindow.destroy()
                return True
            else:
                dialogWindow.destroy()
                return False

    def select_container_to_import_cert(self, liststore):
        # сделать окно выбора контейнера из списка распознанных системой
        # команда из ТГ по экспортированияю контейнера попробовать выполнить автоинсталл,
        # в случае неудачи сделать по БЗ с явным указание открытого ключа
        self.liststore_all_containers = liststore
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("select_container_to_import_cert")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("select_container_to_import_cert_treeview")
        treeview.set_model(self.liststore_all_containers)
        renderer_text = Gtk.CellRendererText()
        col1_text = _("Containers")
        column_text = Gtk.TreeViewColumn(col1_text, renderer_text, text=0)
        treeview.append_column(column_text)
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_all_toggled)
        col2_text = _("Selected")
        column_toggle = Gtk.TreeViewColumn(col2_text, renderer_toggle, active=1)
        treeview.append_column(column_toggle)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def install_container_from_token(self, liststore):
        # сделать окно выбора контейнера из списка распознанных системой
        # команда из ТГ по экспортированияю контейнера попробовать выполнить автоинсталл,
        # в случае неудачи сделать по БЗ с явным указание открытого ключа
        self.liststore_containers = liststore
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("install_container_from_token")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("liststore_containers_treeview")
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Контейнеры", renderer_text, text=0)
        treeview.append_column(column_text)
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)
        treeview.set_model(self.liststore_containers)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def choose_dest_stores(self, liststore):
        self.liststore_dest_stores = liststore

        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("choose_dest_stores")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("choose_dest_stores_treeview")

        treeview.set_model(self.liststore_dest_stores)
        renderer_text = Gtk.CellRendererText()
        col1_text = _("Vaults")
        column_text = Gtk.TreeViewColumn(col1_text, renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_dest_toggled)
        col2_text = _("Selected")
        column_toggle = Gtk.TreeViewColumn(col2_text, renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def choose_open_cert_to_close_container(self, container):
        text = _("Select user certificate")
        dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Сертификаты")
        filter.add_mime_type("Сертификаты")
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        dialog.add_filter(filter)
        domain_name = os.popen("echo $USERNAME").readlines()[0].strip()
        if "\\" in domain_name:
            domain_name = domain_name.split("\\")[1]
        elif "@" in domain_name:
            domain_name = domain_name.split("@")[0]
        find_name = os.popen(f"find /home/ -maxdepth 2 -name *{domain_name}*").readlines()
        dialog.set_current_folder(f"{find_name}")
        dialog.set_select_multiple(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            if file_name:
                output = os.popen(
                    f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -file '{file_name}' -cont '{container}'").readlines()
                for l in output:
                    if "[ErrorCode: 0x00000000]" in l:
                        info = get_cert_info_from_file(file_name)
                        CA_LIST_STR = ""
                        CDP_LIST_STR = ""
                        try:
                            if type(info[0]) == str and len(info[0]) > 0:
                                CA_LIST_STR = info[0]
                            if type(info[1]) == str and len(info[1]) > 0:
                                CDP_LIST_STR = info[1]
                        except IndexError:
                            pass
                        if CA_LIST_STR != "" or CDP_LIST_STR != "":
                            if self.ask_about_extras(self) == Gtk.ResponseType.OK:
                                strk_out = []
                                errors_ca = []
                                success_ca = []
                                errors_cdp = []
                                success_cdp = []
                                if CA_LIST_STR != "":

                                    for ca in CA_LIST_STR.split("\n"):
                                        out = install_CA_extra(ca, "uRoot")
                                        success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                        time.sleep(2)
                                if CDP_LIST_STR != "":
                                    if CA_LIST_STR != "":
                                        strk_out += "\n"

                                    for cdp in CDP_LIST_STR.split("\n"):
                                        out = install_CDP_extra(cdp, "uRoot")
                                        success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                        time.sleep(2)
                                if len(success_ca) > 0:
                                    text = _("Successfully installed root certificates:")
                                    strk_out.append(text)
                                    for succ in success_ca:
                                        strk_out.append(f"{succ}")

                                if len(success_cdp) > 0:
                                    text = _("Successfully installed CRLs:")
                                    strk_out.append(text)
                                    for succ in success_cdp:
                                        strk_out.append(f"{succ}")

                                if len(errors_ca) > 0:
                                    text = _("Error installing root certificates:")
                                    strk_out.append(text)
                                    for err in errors_ca:
                                        strk_out.append(f"{err[0]}\n{err[1]}")

                                if len(errors_cdp) > 0:
                                    if len(success_ca) > 0 or len(success_cdp) > 0 or len(errors_ca) > 0:
                                        strk_out += "\n"
                                    text = _("Error installing CRLs:")
                                    strk_out.append(text)
                                    for err in errors_cdp:
                                        strk_out.append(f"{err[0]}\n{err[1]}")

                                view = ViewCertOutput()
                                view.viewcertoutput_model(strk_out, "", "")
                            os.system("rm -rf /tmp/token-manager/")
                        else:
                            text = _("Certificate installed successfully")
                            self.info_class.print_simple_info(text)
                        return [True]
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return [False, "Отменено пользователем"]

    def install_local_cert_to_container(self, widget):
        text = _("Select user certificate")
        dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Сертификаты")
        filter.add_mime_type("Сертификаты")
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        dialog.add_filter(filter)
        domain_name = os.popen("echo $USERNAME").readlines()[0].strip()
        if "\\" in domain_name:
            domain_name = domain_name.split("\\")[1]
        elif "@" in domain_name:
            domain_name = domain_name.split("@")[0]
        find_name = os.popen(f"find /home/ -maxdepth 2 -name *{domain_name}*").readlines()
        dialog.set_current_folder(f"{find_name}")
        dialog.set_select_multiple(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            if file_name:
                containers = Gtk.ListStore(str, bool)
                conts = get_ALL_certs()
                for cont in conts[0]:
                    if len(cont) > 0:
                        containers.append([cont.split("|")[0].strip(), False])
                if len(containers) > 0:
                    if self.install_container_from_token(containers):
                            selected_containers = self.return_liststore_containers()
                            name = ""
                            selected = 0
                            sel_cont = None
                            for cont in selected_containers:
                                if cont[1]:
                                    selected += 1
                                    sel_cont = cont[0]
                            if selected > 1:
                                text = _("You need to select 1 container\nto set up binding")
                                self.print_error(text)
                            else:
                                for cont in conts[0]:
                                    cont = cont.split("|")
                                    if sel_cont == cont[0].strip():
                                        sel_cont = cont[1].strip()
                                        break
                                output = subprocess.Popen([f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -file '{file_name}' -cont '{sel_cont}'"],
                                                            stdout=subprocess.PIPE,
                                                            stderr=subprocess.PIPE, shell=True)
                                output, error = output.communicate()
                                if "[ErrorCode: 0x00000000]" in output.decode('utf-8'):
                                    info = get_cert_info_from_file(file_name)
                                    CA_LIST_STR = ""
                                    CDP_LIST_STR = ""
                                    try:
                                        if type(info[0]) == str and len(info[0]) > 0:
                                            CA_LIST_STR = info[0]
                                        if type(info[1]) == str and len(info[1]) > 0:
                                            CDP_LIST_STR = info[1]
                                    except IndexError:
                                        pass
                                    if CA_LIST_STR != "" or CDP_LIST_STR != "":
                                        if self.ask_about_extras(self) == Gtk.ResponseType.OK:
                                            strk_out = []
                                            errors_ca = []
                                            success_ca = []
                                            errors_cdp = []
                                            success_cdp = []
                                            if CA_LIST_STR != "":

                                                for ca in CA_LIST_STR.split("\n"):
                                                    out = install_CA_extra(ca)
                                                    success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                                    time.sleep(2)
                                            if CDP_LIST_STR != "":
                                                if CA_LIST_STR != "":
                                                    strk_out += "\n"

                                                for cdp in CDP_LIST_STR.split("\n"):
                                                    out = install_CDP_extra(cdp)
                                                    success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                                    time.sleep(2)
                                            if len(success_ca) > 0:
                                                text = _("Successfully installed root certificates:")
                                                strk_out.append(text)
                                                for succ in success_ca:
                                                    strk_out.append(f"{succ}")

                                            if len(success_cdp) > 0:
                                                text = _("Successfully installed CRLs:")
                                                strk_out.append(text)
                                                for succ in success_cdp:
                                                    strk_out.append(f"{succ}")

                                            if len(errors_ca) > 0:
                                                text = _("Error installing root certificates:")
                                                strk_out.append(text)
                                                for err in errors_ca:
                                                    strk_out.append(f"{err[0]}\n{err[1]}")

                                            if len(errors_cdp) > 0:
                                                text = _("Error installing CRLs:")
                                                strk_out.append(text)
                                                for err in errors_cdp:
                                                    strk_out.append(f"{err[0]}\n{err[1]}")

                                            view = ViewCertOutput()
                                            view.viewcertoutput_model(strk_out, "", "")
                                        os.system("rm -rf /tmp/token-manager/")
                                    else:
                                        text = _("The certificate was successfully associated with the container.")
                                        self.print_simple_info(text)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def install_cert_from_or_to_container(self, container, name_cont):
        # Требуется попробовать получить открытую часть хранилища автоматически, установленного локально в HDIMAGE
        self.output_code_token = False
        name = container.split("\\")[-1:][0].strip()
        csptest = subprocess.Popen(['/opt/cprocsp/bin/%s/csptest' % arch, '-keyset', '-enum_cont', '-unique', '-fqcn',
                                    '-verifyc'], stdout=subprocess.PIPE)
        output = csptest.communicate()[0].decode('cp1251').encode('utf-8').decode("utf-8")
        certs = []
        for line in output.split("\n"):
            if name_cont in line and name in line:
                certs.append(line)
        for cert in certs:
            cert = cert.split("|")[1].strip()
            output = os.popen(f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -cont '{cert}'").readlines()
            for l in output:
                if "[ErrorCode: 0x00000000]" in l:
                    self.output_code_token = True
                    cert_info = list_cert(cert)
                    line = cert_info[0]
                    CA_LIST_STR = ""
                    CDP_LIST_STR = ""
                    try:
                        if type(line[9]) == str and len(line[9]) > 0:
                            CA_LIST_STR = line[9]
                        if type(line[10]) == str and len(line[10]) > 0:
                            CDP_LIST_STR = line[10]
                    except IndexError:
                        pass
                    if CA_LIST_STR != "" or CDP_LIST_STR != "":
                        if self.ask_about_extras(self) == Gtk.ResponseType.OK:
                            strk_out = []
                            errors_ca = []
                            success_ca = []
                            errors_cdp = []
                            success_cdp = []
                            if CA_LIST_STR != "":
                                for ca in CA_LIST_STR.split("\n"):
                                    out = install_CA_extra(ca, "uRoot")
                                    success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                    time.sleep(2)
                            if CDP_LIST_STR != "":
                                 for cdp in CDP_LIST_STR.split("\n"):
                                    out = install_CDP_extra(cdp, "uRoot")
                                    success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                    time.sleep(2)
                            if len(success_ca) > 0:
                                text = _("Successfully installed root certificates:")
                                strk_out.append(text)
                                for succ in success_ca:
                                    strk_out.append(f"{succ}")

                            if len(success_cdp) > 0:
                                text = _("Successfully installed CRLs:")
                                strk_out.append(text)
                                for succ in success_cdp:
                                    strk_out.append(f"{succ}")

                            if len(errors_ca) > 0:
                                text = _("Error installing root certificates:")
                                strk_out.append(text)
                                for err in errors_ca:
                                    strk_out += f"{err[0]}\n{err[1]}\n"

                            if len(errors_cdp) > 0:
                                text = _("Error installing CRLs:")
                                strk_out.append(text)
                                for err in errors_cdp:
                                    strk_out.append(f"{err[0]}\n{err[1]}")

                            view = ViewCertOutput()
                            view.viewcertoutput_model(strk_out, "", "")
                        os.system("rm -rf /tmp/token-manager/")
                    else:
                        text = _("Container successfully copied\nand associated with the certificate.")
                        self.info_class.print_simple_info(text)
                    return True
        # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
        if not self.output_code_token:
            text = _("Select user certificate")
            dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                           action=Gtk.FileChooserAction.OPEN,
                                           )
            dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                               Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
            filter = Gtk.FileFilter()
            text = _("Certificates")
            filter.set_name(f"{text}")
            filter.add_mime_type(text)
            filter.add_pattern("*.cer")
            filter.add_pattern("*.CER")
            dialog.add_filter(filter)
            domain_name = os.popen("echo $USERNAME").readlines()[0].strip()
            if "\\" in domain_name:
                domain_name = domain_name.split("\\")[1]
            elif "@" in domain_name:
                domain_name = domain_name.split("@")[0]
            find_name = os.popen(f"find /home/ -maxdepth 2 -name *{domain_name}*").readlines()
            dialog.set_current_folder(f"{find_name}")
            dialog.set_select_multiple(False)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_name = dialog.get_filename()
                dialog.destroy()
                if file_name:
                    output = os.popen(
                        f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -file '{file_name}' -cont '{container}'").readlines()
                    for l in output:
                        if "[ErrorCode: 0x00000000]" in l:
                            info = get_cert_info_from_file(file_name)
                            CA_LIST_STR = ""
                            CDP_LIST_STR = ""
                            try:
                                if type(info[0]) == str and len(info[0]) > 0:
                                    CA_LIST_STR = info[0]
                                if type(info[1]) == str and len(info[1]) > 0:
                                    CDP_LIST_STR = info[1]
                            except IndexError:
                                pass
                            if CA_LIST_STR != "" or CDP_LIST_STR != "":
                                if self.ask_about_extras(self) == Gtk.ResponseType.OK:
                                    strk_out = []
                                    errors_ca = []
                                    success_ca = []
                                    errors_cdp = []
                                    success_cdp = []
                                    if CA_LIST_STR != "":

                                        for ca in CA_LIST_STR.split("\n"):
                                            out = install_CA_extra(ca, "uRoot")
                                            success_ca.append(out[0]) if out[1] == 0 else errors_ca.append(out[0])
                                            time.sleep(2)
                                    if CDP_LIST_STR != "":
                                        for cdp in CDP_LIST_STR.split("\n"):
                                            out = install_CDP_extra(cdp, "uRoot")
                                            success_cdp.append(out[0]) if out[1] == 0 else errors_cdp.append(out[0])
                                            time.sleep(2)
                                    if len(success_ca) > 0:
                                        text = _("Successfully installed root certificates:")
                                        strk_out += text
                                        for succ in success_ca:
                                            strk_out.append(f"{succ}")

                                    if len(success_cdp) > 0:
                                        if len(success_ca) > 0:
                                            strk_out += "\n"
                                        text = _("Successfully installed CRLs:")
                                        strk_out.append(text)
                                        for succ in success_cdp:
                                            strk_out.append(f"{succ}")
                                    if len(errors_ca) > 0:
                                        text = _("Error installing root certificates:")
                                        strk_out.append(text)
                                        for err in errors_ca:
                                            strk_out += f"{err[0]}\n{err[1]}\n"

                                    if len(errors_cdp) > 0:
                                        if len(success_ca) > 0 or len(success_cdp) > 0 or len(errors_ca) > 0:
                                            strk_out += "\n"
                                        text = _("Error installing CRLs:")
                                        strk_out.append(text)
                                        for err in errors_cdp:
                                            strk_out.append(f"{err[0]}\n{err[1]}")

                                    view = ViewCertOutput()
                                    view.viewcertoutput_model(strk_out, "", "")
                                os.system("rm -rf /tmp/token-manager/")
                            else:
                                text = _("Container successfully copied\nand associated with the certificate.")
                                self.info_class.print_simple_info(text)
                            self.output_code_token = True
                            return True
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.output_code_token = False
                return False
    def install_new_cert_to_container(self, container):
        text = _("Select user certificate")
        dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        text = _("Certificates")
        filter.set_name(f"{text}")
        filter.add_mime_type(text)
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        dialog.add_filter(filter)
        domain_name = os.popen("echo $USERNAME").readlines()[0].strip()
        if "\\" in domain_name:
            domain_name = domain_name.split("\\")[1]
        elif "@" in domain_name:
            domain_name = domain_name.split("@")[0]
        find_name = os.popen(f"find /home/ -maxdepth 2 -name *{domain_name}*").readlines()
        dialog.set_current_folder(f"{find_name[0].strip()}")
        dialog.set_select_multiple(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            if file_name:
                p = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-inst', '-file', file_name, '-cont',
                                      container, '-inst_to_cont'], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                output, error = p.communicate()
                if p.returncode != 0:
                    return error.decode("utf-8").strip()
                else:
                    return "success"
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return "Отменено пользователем"

    def choose_folder_dialog(self, widget):
        text = _("Select directory")
        dialog = Gtk.FileChooserDialog(title=text, parent=self,
                                       action=Gtk.FileChooserAction.SELECT_FOLDER,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           text, Gtk.ResponseType.OK)
        dialog.set_default_size(800, 400)
        # если на ПК не обнаружен СН то стандартная папка по умолчанию /run/media/USERNAME, иначе будет другая папка
        # по дефолту - /media/
        dialog.set_current_folder(f"/home")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            return file_name
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return False
        else:
            dialog.destroy()
            return False

    def install_container_from_flash(self, liststore):
        self.liststore_flashes = liststore
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("install_container_from_flash")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("install_container_from_flash_treeview")

        treeview.set_model(self.liststore_flashes)

        renderer_text = Gtk.CellRendererText()
        col1_text = _("Containers")
        column_text = Gtk.TreeViewColumn(col1_text, renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled_flash)
        col2_text = _("Selected")
        column_toggle = Gtk.TreeViewColumn(col2_text, renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def call_secretnet_configs(self, for_what, udev):
        file = f"/etc/udev/rules.d/87-{udev}_usb.rules"
        if not os.path.exists(file):
            temp_builder = Gtk.Builder()
            temp_builder.set_translation_domain('token_manager')
            # temp_builder.add_from_file('../../data/ui/templates.glade')
            temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

            dialogWindow = temp_builder.get_object("call_secretnet_configs")
            dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OK, Gtk.ResponseType.OK)
            text = _("Configure udev rule for ")
            dialogWindow.set_title(text+for_what)
            pinEntry = temp_builder.get_object("call_secretnet_configs_entry")
            pinEntry.set_visibility(False)
            response = dialogWindow.run()
            if response == Gtk.ResponseType.OK:
                pin = pinEntry.get_text()
                ROOTPSW = pin  # сделать окно диалог с запросом рут пароля.
                os.system("""su - root -c 'cat << EOF > /etc/udev/rules.d/87-domain_usb.rules \n""" \
                          """ENV{ID_FS_USAGE}=="filesystem|other|crypto", ENV{UDISKS_FILESYSTEM_SHARED}="1"\n""" \
                          """EOF'""" + f"<<< '{ROOTPSW}'")
                os.system(f"""su - root -c 'udevadm control --reload' <<< '{ROOTPSW}' """)
                dialogWindow.destroy()
                return "just_installed"
            else:
                dialogWindow.destroy()
                return "canceled"
        else:
            return "installed"

    def install_container_from_hdimage(self, liststore):
        self.liststore_hdimage_containers = liststore
        temp_builder = Gtk.Builder()
        temp_builder.set_translation_domain('token_manager')
        # temp_builder.add_from_file('../../data/ui/templates.glade')
        temp_builder.add_from_file(f'{appdir}/usr/share/token_manager/ui/templates.glade') if appdir else temp_builder.add_from_file('/usr/share/token_manager/ui/templates.glade')

        dialogWindow = temp_builder.get_object("install_container_from_hdimage")
        dialogWindow.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK)
        treeview = temp_builder.get_object("install_container_from_hdimage_treeview")
        renderer_text = Gtk.CellRendererText()
        col1_text = _("Containers")
        column_text = Gtk.TreeViewColumn(col1_text, renderer_text, text=0)
        treeview.append_column(column_text)
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_hdimage_toggled)
        col2_text = _("Selected")
        column_toggle = Gtk.TreeViewColumn(col2_text, renderer_toggle, active=1)
        treeview.append_column(column_toggle)
        treeview.set_model(self.liststore_hdimage_containers)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def return_liststore_containers(self):
        return self.liststore_containers

    def return_liststore_all_containers(self):
        return self.liststore_all_containers

    def return_liststore_flashes(self):
        return self.liststore_flashes

    def return_liststore_dest_stores(self):
        return self.liststore_dest_stores

    def return_liststore_hdimage_containers(self):
        return self.liststore_hdimage_containers

    def on_cell_toggled(self, widget, path):
        self.liststore_containers[path][1] = not self.liststore_containers[path][1]

    def on_cell_all_toggled(self, widget, path):
        self.liststore_all_containers[path][1] = not self.liststore_all_containers[path][1]

    def on_cell_hdimage_toggled(self, widget, path):
        self.liststore_hdimage_containers[path][1] = not self.liststore_hdimage_containers[path][1]

    def on_cell_dest_toggled(self, widget, path):
        self.liststore_dest_stores[path][1] = not self.liststore_dest_stores[path][1]

    def on_cell_toggled_flash(self, widget, path):
        self.liststore_flashes[path][1] = not self.liststore_flashes[path][1]

def main():
    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_path(f"{appdir}/usr/share/token_manager/ui/style.css") if appdir else  provider.load_from_path("/usr/share/token_manager/ui/style.css")
    # provider.load_from_path("../../data/ui/style.css")

    Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    class_win = TokenUI()
    class_win.window.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    window = main()
