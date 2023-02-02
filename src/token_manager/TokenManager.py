#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Copyright (c) 2017 Борис Макаренко
Copyright (c) 2020-2022 Владлен Мурылев

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
Copyright (c) 2020-2022 Vladlen Murylev

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
import os, gi, re, subprocess, platform, sys, webbrowser
import time

import chardet

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from datetime import datetime

from pathlib import Path

VERSION = "4.2"

GUI_USERS = os.popen("w | grep -c xdm").readline().strip()
appdir = os.popen("echo $APPDIR").readline().strip()

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


path = os.path.abspath(__file__)
global_import = re.sub("/modules/administration/token-manager-gtk.py", "", path)
path = global_import + "/icons/"
root_png = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x02\x01\x03\xd2\x03\x01\x04\xfe\x03\x01\x04\xff\x03\x01' \
           b'\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
           b'\x03\x01\x04\xff\x03\x01\x04\xf8\x03\x01\x03\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02Z\x02\x01\x04\xba\x00\x00\x00\x01\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x03\x01\x04\xfb\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x03\x01\x04\xff\x00\x00\x00\x02\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab' \
           b'\x00\x00\x00\x00\x03\x01\x03\x89\x03\x01\x04\xaa\x03\x01\x04\xaa\x03\x01\x04\xaa\x03\x01\x04\xaa\x03' \
           b'\x01\x04\xaa\x03\x01\x04\xaa\x03\x01\x04\xaa\x03\x00\x03G\x00\x00\x00\x08\x03\x01\x04\xff\x00\x00\x00' \
           b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02' \
           b'\x01\x04\xab\x00\x00\x00\x00\x04\x00\x045\x03\x00\x03D\x03\x00\x03D\x03\x00\x03D\x03\x00\x03D\x03\x00' \
           b'\x03D\x03\x00\x03D\x03\x00\x03D\x00\x00\x00\x1a\x00\x00\x00\x08\x03\x01\x04\xff\x00\x00\x00\x01\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04' \
           b'\xab\x00\x00\x00\x00\x00\x00\x00\x1d\x05\x00\x053\x05\x00\x053\x05\x00\x053\x05\x00\x053\x05\x00\x053' \
           b'\x05\x00\x053\x05\x00\x053\x00\x00\x00\t\x00\x00\x00\x08\x03\x01\x04\xff\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00' \
           b'\x00\x00\x00\x02\x01\x04\xab\x02\x01\x03\xcc\x02\x01\x03\xcc\x02\x01\x03\xcc\x02\x01\x03\xcc\x02\x01' \
           b'\x03\xcc\x02\x01\x03\xcc\x02\x01\x03\xcc\x02\x00\x02\\\x00\x00\x00\x08\x03\x01\x04\xff\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01' \
           b'\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x03\x01\x04\xff' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02' \
           b'\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07#\x03\x00\x03E\x00\x00\x00\x00\x00\x00\x00\x05\x03\x01' \
           b'\x03\xdd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x03\x00\x03\x80\x03\x01\x03\x8d\x03\x01\x03\xd8\x03\x01\x04\xe5\x03\x01\x03\x96\x03\x01\x03' \
           b'\x97\x00\x00\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x0e\x03\x01\x04\xe7\x02\x00\x04h\x03\x01\x03\x8e\x03\x01\x03\x9c\x02\x00\x05f\x02\x01' \
           b'\x03\xc7\x02\x00\x02Y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x06(\x02\x01\x03\xc7\x04\x00\x04g\x03\x01\x04\xf6\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x02' \
           b'\x00\x04{\x03\x01\x03\xd6\x02\x00\x02V\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00' \
           b'\x03K\x03\x01\x03\xdb\x03\x01\x04\xa4\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
           b'\x03\x01\x04\xed\x03\x01\x03\x92\x03\x01\x03\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\n\x02\x01\x03\xc1\x02\x01\x04\xbd\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03' \
           b'\x01\x04\xff\x03\x01\x04\xfd\x02\x00\x04|\x03\x00\x03U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02_\x02\x01\x04\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x02\x00\x05`\x03\x01\x04\xef\x02\x00\x04\x7f\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
           b'\x03\x01\x04\xff\x02\x01\x03\xc3\x02\x01\x04\xaf\x03\x01\x04\xaa\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03S\x02\x01\x03\xcd\x03\x00\x03U\x03\x00\x03U\x03' \
           b'\x00\x03U\x00\x00\x05-\x03\x01\x03\x98\x03\x01\x03\x9b\x03\x01\x04\xa6\x03\x01\x04\xff\x03\x01\x04\xff' \
           b'\x02\x01\x03\xd0\x02\x00\x04k\x02\x01\x03\xc1\x00\x00\x07$\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x03\x01\x03\x96\x02\x01\x04\xbb\x02\x01\x04\xbb' \
           b'\x02\x01\x04\xbb\x02\x00\x04i\x05\x00\x051\x03\x01\x04\xf8\x02\x01\x03\xc4\x02\x00\x04z\x02\x00\x06x' \
           b'\x03\x01\x04\xa1\x03\x01\x04\xfe\x02\x00\x05d\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x02\x00\x04t\x03\x01\x04\xef\x03\x00\x03\x81\x04\x00\x04\x7f\x02\x01\x04\xbc\x03' \
           b'\x01\x04\xe8\x04\x00\x04w\x03\x00\x03\x85\x02\x01\x03\xc0\x02\x01\x04\xb6\x00\x00\x00\x08\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x02\x03\x01\x03\x9e\x03\x01\x04\xf1\x03\x01\x04\xfa\x03\x00\x03T\x00\x00' \
           b'\x00\x07\x00\x00\x00\x15\x00\x00\x07#\x03\x01\x04\xe1\x03\x01\x04\xff\x02\x01\x04\xb4\x00\x00\x06*\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x03\x9c\x03\x00\x03R\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07!\x02\x01\x03\xcb\x00\x00\x00\x02\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

personal_png = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\xcd\x00\x00\x00\xee\x00\x00\x00\xee\x00\x00\x00\xcc\x00\x00\x00W' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00N\x00\x00\x00\xfe\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\xff\x00\x00\x00\xfe\x00\x00\x00L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xbe\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xed\x00\x00\x00\xff\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xeb\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\xfd\x00\x00' \
               b'\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\xfc\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00' \
               b'\x00\x00\xf9\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00' \
               b'\x00\xff\x00\x00\x00\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\xc8\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00' \
               b'\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00c\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\xb1\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xae\x00\x00\x00\x01\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x03\x00\x00\x00c\x00\x00\x00\xb7\x00\x00\x00\xb7\x00\x00\x00a\x00\x00\x00\x02\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00C\x00\x00\x00' \
               b'\x8e\x00\x00\x00\xbe\x00\x00\x00[\x00\x00\x00\t\x00\x00\x00\t\x00\x00\x00]\x00\x00\x00\xbf\x00\x00' \
               b'\x00\x8e\x00\x00\x00D\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!\x00\x00\x00\xce\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00' \
               b'\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xcf\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\xd1\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xcc\x00' \
               b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00;\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00' \
               b'\x00\x00\xff\x00\x00\x007\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00i\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00h\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00~\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00' \
               b'\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00' \
               b'\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\x8e\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95\x00\x00\x00\xff\x00\x00\x00\xff\x00' \
               b'\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00' \
               b'\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00' \
               b'\x94\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\xb3' \
               b'\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00' \
               b'\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00' \
               b'\x00\xb1\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x002\x00\x00\x00~\x00\x00\x00\xb2\x00\x00\x00\xda\x00\x00\x00\xf0\x00' \
               b'\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xf0\x00\x00\x00\xda\x00\x00\x00\xb2\x00\x00\x00}\x00\x00' \
               b'\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

usb_token_png = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x0c\x02\x01\x04\xb0\x05\x00\x053\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x02\x01\x03\xc1\x03\x01\x03\x82\x03\x01\x03\xd7\x05' \
                b'\x00\x053\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x02\x01\x03\xc2\x02\x00\x04x\x03\x01\x03\x96' \
                b'\x04\x00\x048\x03\x01\x03\xd8\x05\x00\x053\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x02\x01\x03\xc2\x02\x00\x05f\x00\x00\x06*' \
                b'\x03\x01\x04\xeb\x03\x01\x03\x82\x05\x00\x05-\x03\x01\x03\xda\x05\x00\x053\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x06(\x02\x01\x03\xc4\x02\x00\x04g\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x06(\x00\x00\x06*\x03\x01\x04\xa3\x04\x00\x04:\x03\x01\x03\xdb\x05' \
                b'\x00\x053\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x02\x01\x03\xc7\x03\x01\x04\xff\x03\x01\x04\xff\x02\x01' \
                b'\x03\xc0\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x05/\x03\x01\x04\xeb\x02\x00\x05b' \
                b'\x03\x01\x03\x9c\x03\x01\x04\xa4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x03\x01\x03\xdc\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x03\xd9\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x17\x03\x01\x03\x87\x02\x01\x04\xb2\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x03\x01\x03\xdd\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x03\xdb' \
                b'\x00\x00\x00\x1c\x00\x00\x00\x00\x03\x01\x03\x88\x02\x01\x04\xb1\x00\x00\x00\x06\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x03\x01\x03\xdd' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x02\x01\x03\xc7\x03\x01\x03\x8b\x02\x01\x04\xaf\x00\x00\x00\x06' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f' \
                b'\x03\x01\x03\xde\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x02\x01\x04\xae' \
                b'\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x07$\x03\x01\x04\xe3\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03' \
                b'\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03' \
                b'\x01\x04\xff\x05\x00\x052\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00 \x03\x01\x03\xdf\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04' \
                b'\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04' \
                b'\xff\x03\x01\x04\xff\x03\x01\x03\xd5\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x18\x03\x01\x04\xe0\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04' \
                b'\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04' \
                b'\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xea\x05\x00\x05-\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x04\xa3\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xea\x05\x00\x05-\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x04\xe1\x03' \
                b'\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03' \
                b'\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xea\x05\x00\x05-\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x02\x01\x03\xc3\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01' \
                b'\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xe9\x05\x00' \
                b'\x05,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03@\x03\x01\x04\xfc\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xe9' \
                b'\x05\x00\x05+\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03K\x03\x01' \
                b'\x04\xf8\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01' \
                b'\x04\xe4\x00\x00\x06%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x03\x00\x03J\x03\x01\x04\xf8\x03\x01\x04\xff\x03\x01\x04\xff\x03\x01\x04\xff' \
                b'\x03\x01\x04\xe4\x00\x00\x06%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03@\x02\x01\x03\xcf\x03\x01' \
                b'\x04\xf6\x02\x01\x04\xb5\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'


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
    output = certmgr.communicate()[0]
    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
        m = re.findall(
            r'(\d+)-{7}\n'
            r'Издатель.*?'
            r'CN=(.+?)[\n,].*?'
            r'Субъект.*?CN=(.+?)[\n,].*?'
            r'Серийный номер.*?(0x.+?)\n'
            r'SHA1 отпечаток.*?(.+?)\n.*?'
            r'Выдан.*?(\d.+?)UTC\n'
            r'Истекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
        m = re.findall(
            r'(\d+)-{7}\nИздатель.*?CN=(.+?)[\n,].*?'
            r'Субъект.*?CN=(.+?)[\n,].*?'
            r'Серийный номер.*?(0x.+?)\n'
            r'Хэш SHA1.*?(.+?)\n.*?'
            r'Выдан.*?(\d.+?)UTC\n'
            r'Истекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        m = re.findall(
            r'(\d+)-{7}\n'
            r'Issuer.*?CN=(.+?)[\n,].*?'
            r'Subject.*?CN=(.+?)[\n,].*?'
            r'Serial.*?(0x.+?)\n'
            r'SHA1 Hash.*?(.+?)\n.*?'
            r'Not valid before.*?(\d.+?)UTC\n'
            r'Not valid after.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
        m = re.findall(
            r'(\d+)-{7}\n'
            r'Издатель.*?CN=(.+?)[\n,].*?'
            r'Субъект.*?CN=(.+?)[\n,].*?'
            r'Серийный номер.*?(0x.+?)\n'
            r'Хэш SHA1.*?(.+?)\n.*?'
            r'Выдан.*?(\d.+?)UTC\n'
            r'Истекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    else:
        m = re.findall(
            r'(\d+)-{7}\n'
            r'Issuer.*?CN=(.+?)[\n,].*?'
            r'Subject.*?CN=(.+?)[\n,].*?'
            r'Serial.*?(0x.+?)\n'
            r'SHA1 Hash.*?(.+?)\n.*?'
            r'Not valid before.*?(\d.+?)UTC\n'
            r'Not valid after.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
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
    output = certmgr.communicate()[0]
    if versiontuple(get_cspversion()[2]) > versiontuple("5.0.11455"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'Выпущен.*?: (\d.+?)UTC\n'
                       r'Истекает.*?: (\d.+?)UTC',
                       output.decode('utf-8'),
                       re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'ThisUpdate: (\d.+?)UTC\n'
                       r'NextUpdate: (\d.+?)UTC',
                       output.decode('utf-8'),
                       re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'Выпущен.*?: (\d.+?)UTC\n'
                       r'Истекает.*?: (\d.+?)UTC',
                       output.decode('utf-8'),
                       re.MULTILINE + re.DOTALL)
    else:
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'ThisUpdate: (\d.+?)UTC\n'
                       r'NextUpdate: (\d.+?)UTC',
                       output.decode('utf-8'),
                       re.MULTILINE + re.DOTALL)
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
    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
        regex_string_CA = r'^URL сертификата УЦ.*?: http.*\.crt\n|URL сертификата УЦ.*?: http.*\.cer'
        regex_string_CDP = r'^URL списка отзыва.*?: http.*\.crl\n'
        resub_string_CA = r'URL сертификата УЦ.*?: '
        resub_string_CDP = r'URL списка отзыва.*?: '
    elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
        regex_string_CA = r'^URL сертификата УЦ.*?: http.*\.crt\n|URL сертификата УЦ.*?: http.*\.cer'
        regex_string_CDP = r'^URL списка отзыва.*?: http.*\.crl\n'
        resub_string_CA = r'URL сертификата УЦ.*?: '
        resub_string_CDP = r'URL списка отзыва.*?: '
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        regex_string_CA = r'^CA cert URL.*?: http.*\.crt\n|URL сертификата УЦ.*?: http.*\.cer'
        regex_string_CDP = r'^CDP.*?: http.*\.crl\n'
        resub_string_CA = r'CA cert URL.*?: '
        resub_string_CDP = r'CDP.*?: '
    elif versiontuple("4.0.9971") <= versiontuple(get_cspversion()[2]) < versiontuple("5.0.10003"):
        regex_string_CA = r'^URL сертификата УЦ.*?: http.*\.crt\n|URL сертификата УЦ.*?: http.*\.cer'
        regex_string_CDP = r'^URL списка отзыва.*?: http.*\.crl\n'
        resub_string_CA = r'URL сертификата УЦ.*?: '
        resub_string_CDP = r'URL списка отзыва.*?: '
    else:
        regex_string_CA = r'^CA cert URL.*?: http.*\.crt\n|URL сертификата УЦ.*?: http.*\.cer'
        regex_string_CDP = r'^CDP.*?: http.*\.crl\n'
        resub_string_CA = r'CA cert URL.*?: '
        resub_string_CDP = r'CDP.*?: '
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
        if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
            m = re.findall(
                r'(\d+)-{7}\n'
                r'Издатель.*?: (.+?)\n.*?'
                r'Субъект.*?: (.+?)\n.*?'
                r'Серийный номер.*?: (0x\w+?)\n'
                r'SHA1 отпечаток.*?(\w+?)\n.*?'
                r'Идентификатор ключа.*?: (.+?)\n.*?'
                r'Выдан.*?(\d.+?)UTC\n'
                r'Истекает.*?(\d.+?)UTC',
                output, re.MULTILINE + re.DOTALL)
        elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
            m = re.findall(
                r'(\d+)-{7}\n'
                r'Издатель.*?: (.+?)\n.*?'
                r'Субъект.*?: (.+?)\n.*?'
                r'Серийный номер.*?: (0x\w+?)\n'
                r'Хэш SHA1.*?(\w+?)\n.*?'
                r'Идентификатор ключа.*?: (.+?)\n.*?'
                r'Выдан.*?(\d.+?)UTC\n'
                r'Истекает.*?(\d.+?)UTC',
                output, re.MULTILINE + re.DOTALL)
        elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
            m = re.findall(
                r'(\d+)-{7}\n'
                r'Issuer.*?: (.+?)\n.*?'
                r'Subject.*?: (.+?)\n.*?'
                r'Serial.*?: (0x\w+?)\n'
                r'SHA1 Hash.*?(\w+?)\n.*?'
                r'SubjKeyID.*?: (.+?)\n.*?'
                r'Not valid before.*?(\d.+?)UTC\n'
                r'Not valid after.*?(\d.+?)UTC',
                output, re.MULTILINE + re.DOTALL)
        elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
            m = re.findall(
                r'(\d+)-{7}\n'
                r'Издатель.*?: (.+?)\n.*?'
                r'Субъект.*?: (.+?)\n.*?'
                r'Серийный номер.*?: (0x\w+?)\n'
                r'Хэш SHA1.*?(\w+?)\n.*?'
                r'Идентификатор ключа.*?: (.+?)\n.*?'
                r'Выдан.*?(\d.+?)UTC\n'
                r'Истекает.*?(\d.+?)UTC',
                output, re.MULTILINE + re.DOTALL)
        else:
            m = re.findall(
                r'(\d+)-{7}\n'
                r'Issuer.*?: (.+?)\n.*?'
                r'Subject.*?: (.+?)\n.*?'
                r'Serial.*?: (0x\w+?)\n'
                r'SHA1 Hash.*?(\w+?)\n.*?'
                r'SubjKeyID.*?: (.+?)\n.*?'
                r'Not valid before.*?(\d.+?)UTC\n'
                r'Not valid after.*?(\d.+?)UTC',
                output, re.MULTILINE + re.DOTALL)
    else:
        if versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9708"):
            certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-store', store],
                                       stdout=subprocess.PIPE)
        else:
            certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-verbose', '-store', store],
                                       stdout=subprocess.PIPE)
        output = certmgr.communicate()[0].decode('utf-8')
        if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
            lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
            m = []
            counter = 1
            for i in range(1, len(lists), 2):
                lists[i] = f"{counter}-------\n" + lists[i]
                if 'Назначение/EKU' in lists[i]:
                    part1 = re.findall(
                        r'(\d+)-{7}\n'
                        r'Издатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'SHA1 отпечаток.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?',
                        lists[i], re.MULTILINE + re.DOTALL)
                    part1 = list(part1[0])
                    part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                    part2 = [x for x in part2 if x != ''][0]
                    if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                        part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                        part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                    else:
                        part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)

                    for j in range(0, len(part2)):
                        part2[j] = re.sub('\n', '', part2[j])
                        part2[j] = part2[j].strip()
                    part1.append(part2)
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                else:
                    lists[i] = re.findall(
                        r'(\d+)-{7}\n'
                        r'Издатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'SHA1 отпечаток.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?\n',
                        lists[i], re.MULTILINE + re.DOTALL)
                    part1 = list(lists[i][0])
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i][0][0])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                counter += 1
        elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
            lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
            m = []
            counter = 1
            for i in range(1, len(lists), 2):
                lists[i] = f"{counter}-------\n" + lists[i]
                if 'Назначение/EKU' in lists[i]:
                    part1 = re.findall(
                        r'(\d+)-{7}\nИздатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'Хэш SHA1.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?',
                        lists[i],
                        re.MULTILINE + re.DOTALL)
                    part1 = list(part1[0])
                    part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                    part2 = [x for x in part2 if x != ''][0]
                    if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                        part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                        part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                    else:
                        part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)

                    for j in range(0, len(part2)):
                        part2[j] = re.sub('\n', '', part2[j])
                        part2[j] = part2[j].strip()
                    part1.append(part2)
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                else:
                    lists[i] = re.findall(
                        r'(\d+)-{7}\n'
                        r'Издатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'Хэш SHA1.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?\n',
                        output, re.MULTILINE + re.DOTALL)
                    part1 = list(lists[i][0])
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i][0][0])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                counter += 1
        elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
            lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
            m = []
            counter = 1
            for i in range(1, len(lists), 2):
                lists[i] = f"{counter}-------\n" + lists[i]
                if 'Extended Key Usage' in lists[i]:
                    part1 = re.findall(
                        r'(\d+)-{7}\n'
                        r'Issuer.*?: (.+?)\n.*?'
                        r'Subject.*?: (.+?)\n.*?'
                        r'Serial.*?: (0x\w+?)\n'
                        r'SHA1 Hash.*?(\w+?)\n.*?'
                        r'SubjKeyID.*?: (.+?)\n.*?'
                        r'Not valid before.*?(\d.+?)UTC\n'
                        r'Not valid after.*?(\d.+?)UTC.+?\n',
                        lists[i], re.MULTILINE + re.DOTALL)
                    part1 = list(part1[0])
                    part2 = re.split(r'Extended Key Usage', lists[i], re.MULTILINE + re.DOTALL)[1:]
                    part2 = [x for x in part2 if x != ''][0]
                    if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                        part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)[:-1]
                        part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                    else:
                        part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                    for j in range(0, len(part2)):
                        part2[j] = re.sub('\n', '', part2[j])
                        part2[j] = part2[j].strip()
                    part1.append(part2)
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                else:
                    lists[i] = re.findall(
                        r'(\d+)-{7}\n'
                        r'Issuer.*?: (.+?)\n.*?'
                        r'Subject.*?: (.+?)\n.*?'
                        r'Serial.*?: (0x\w+?)\n'
                        r'SHA1 Hash.*?(\w+?)\n.*?'
                        r'SubjKeyID.*?: (.+?)\n.*?'
                        r'Not valid before.*?(\d.+?)UTC\n'
                        r'Not valid after.*?(\d.+?)UTC.+?\n',
                        lists[i], re.MULTILINE + re.DOTALL)
                    part1 = list(lists[i][0])
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i][0][0])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                counter += 1
        elif versiontuple("4.0.9971") <= versiontuple(get_cspversion()[2]) < versiontuple("5.0.10003"):
            lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
            m = []
            counter = 1
            for i in range(1, len(lists), 2):
                lists[i] = f"{counter}-------\n" + lists[i]
                if 'Назначение/EKU' in lists[i]:
                    part1 = re.findall(
                        r'(\d+)-{7}\n'
                        r'Издатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'Хэш SHA1.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?\n',
                        output, re.MULTILINE + re.DOTALL)
                    part1 = list(part1[0])
                    part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                    part2 = [x for x in part2 if x != ''][0]
                    if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                        part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                        part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                    else:
                        part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                    for i in range(0, len(part2)):
                        part2[i] = re.sub('\n', '', part2[i])
                        part2[i] = part2[i].strip()
                    part1.append(part2)
                    m.append(part1)
                else:
                    lists[i] = re.findall(
                        r'(\d+)-{7}\n'
                        r'Издатель.*?: (.+?)\n.*?'
                        r'Субъект.*?: (.+?)\n.*?'
                        r'Серийный номер.*?: (0x\w+?)\n'
                        r'Хэш SHA1.*?(\w+?)\n.*?'
                        r'Идентификатор ключа.*?: (.+?)\n.*?'
                        r'Выдан.*?(\d.+?)UTC\n'
                        r'Истекает.*?(\d.+?)UTC.+?\n',
                        output, re.MULTILINE + re.DOTALL)
                    part1 = list(lists[i][0])
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i][0][0])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                counter += 1
        else:
            lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
            m = []
            counter = 1
            for i in range(1, len(lists), 2):
                lists[i] = f"{counter}-------\n" + lists[i]
                if 'Extended Key Usage' in lists[i]:
                    part1 = re.findall(
                        r'(\d+)-{7}\n'
                        r'Issuer.*?: (.+?)\n.*?'
                        r'Subject.*?: (.+?)\n.*?'
                        r'Serial.*?: (0x\w+?)\n'
                        r'SHA1 Hash.*?(\w+?)\n.*?'
                        r'SubjKeyID.*?: (.+?)\n.*?'
                        r'Not valid before.*?(\d.+?)UTC\n'
                        r'Not valid after.*?(\d.+?)UTC.+?\n',
                        lists[i], re.MULTILINE + re.DOTALL)

                    part1 = list(part1[0])
                    part2 = re.split(r'Extended Key Usage', lists[i], re.MULTILINE + re.DOTALL)[1:]
                    part2 = [x for x in part2 if x != ''][0]
                    if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                        part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)[:-1]
                        part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                    else:
                        part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                    for j in range(0, len(part2)):
                        part2[j] = re.sub('\n', '', part2[j])
                        part2[j] = part2[j].strip()
                    part1.append(part2)

                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                    part1.append(certs_UC_str)
                    part1.append(certs_CDP_str)
                    m.append(part1)
                else:
                    lists[i] = re.findall(
                            r'(\d+)-{7}\n'
                            r'Issuer.*?: (.+?)\n.*?'
                            r'Subject.*?: (.+?)\n.*?'
                            r'Serial.*?: (0x\w+?)\n'
                            r'SHA1 Hash.*?(\w+?)\n.*?'
                            r'SubjKeyID.*?: (.+?)\n.*?'
                            r'Not valid before.*?(\d.+?)UTC\n'
                            r'Not valid after.*?(\d.+?)UTC.+?\n',
                            lists[i], re.MULTILINE + re.DOTALL)
                    part1 = list(lists[i][0])
                    certs_UC_str = ""
                    certs_CDP_str = ""
                    certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i][0][0])
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
    output = certmgr.communicate()[0]
    if versiontuple(get_cspversion()[2]) > versiontuple("5.0.11455"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'Выпущен.+?: (\d.+?)UTC\n'
                       r'Истекает.+?: (\d.+?)UTC',
                       output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'ThisUpdate: (\d.+?)UTC\nNextUpdate: (\d.+?)UTC',
                       output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'Выпущен.+?: (\d.+?)UTC\n'
                       r'Истекает.+?: (\d.+?)UTC',
                       output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    else:
        m = re.findall(r'(\d+)-{7}.+?'
                       r'CN=(.+?)[\n,].*?'
                       r'ThisUpdate: (\d.+?)UTC\n'
                       r'NextUpdate: (\d.+?)UTC',
                       output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    return m


def list_root_certs():
    certmgr = subprocess.Popen(['/opt/cprocsp/bin/%s/certmgr' % arch, '-list', '-store', 'uRoot'],
                               stdout=subprocess.PIPE)
    output = certmgr.communicate()[0]
    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
        m = re.findall(
            r'(\d+)-{7}\n'
            r'Издатель.*?CN=(.+?)[\n,].*?'
            r'Субъект.*?CN=(.+?)[\n,].*?'
            r'Серийный номер.*?(0x.+?)\n'
            r'SHA1 отпечаток.*?(.+?)\n.*?'
            r'Выдан.*?(\d.+?)UTC\n'
            r'Истекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
        m = re.findall(
            r'(\d+)-{7}\nИздатель.*?CN=(.+?)[\n,].*?Субъект.*?CN=(.+?)[\n,].*?Серийный номер.*?(0x.+?)\nХэш SHA1.*?(.+?)\n.*?Выдан.*?(\d.+?)UTC\nИстекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        m = re.findall(
            r'(\d+)-{7}\nIssuer.*?CN=(.+?)[\n,].*?Subject.*?CN=(.+?)[\n,].*?Serial.*?(0x.+?)\nSHA1 Hash.*?(.+?)\n.*?Not valid before.*?(\d.+?)UTC\nNot valid after.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
        m = re.findall(
            r'(\d+)-{7}\nИздатель.*?CN=(.+?)[\n,].*?Субъект.*?CN=(.+?)[\n,].*?Серийный номер.*?(0x.+?)\nХэш SHA1.*?(.+?)\n.*?Выдан.*?(\d.+?)UTC\nИстекает.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
    else:
        m = re.findall(
            r'(\d+)-{7}\nIssuer.*?CN=(.+?)[\n,].*?Subject.*?CN=(.+?)[\n,].*?Serial.*?(0x.+?)\nSHA1 Hash.*?(.+?)\n.*?Not valid before.*?(\d.+?)UTC\nNot valid after.*?(\d.+?)UTC',
            output.decode('utf-8'), re.MULTILINE + re.DOTALL)
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
    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
        lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
        m = []
        counter = 1
        for i in range(1, len(lists), 2):
            lists[i] = f"{counter}-------\n" + lists[i]
            if 'Назначение/EKU' in lists[i]:
                part1 = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'SHA1 отпечаток.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?',
                    lists[i], re.MULTILINE + re.DOTALL)
                part1 = list(part1[0])
                part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                part2 = [x for x in part2 if x != ''][0]
                if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                    part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                    part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                else:
                    part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)

                for j in range(0, len(part2)):
                    part2[j] = re.sub('\n', '', part2[j])
                    part2[j] = part2[j].strip()
                part1.append(part2)

                certs_UC_str = ""
                certs_CDP_str = ""
                certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                part1.append(certs_UC_str)
                part1.append(certs_CDP_str)
                m.append(part1)
            else:
                lists[i] = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'SHA1 отпечаток.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?\n',
                    lists[i], re.MULTILINE + re.DOTALL)
                m.append(lists[i][0])
            counter += 1
    elif versiontuple("5.0.11455") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.12000"):
        lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
        m = []
        counter = 1
        for i in range(1, len(lists), 2):
            lists[i] = f"{counter}-------\n" + lists[i]
            if 'Назначение/EKU' in lists[i]:
                part1 = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'Хэш SHA1.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?', lists[i],
                    re.MULTILINE + re.DOTALL)
                part1 = list(part1[0])
                part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                part2 = [x for x in part2 if x != ''][0]
                if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                    part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                    part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                else:
                    part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)

                for j in range(0, len(part2)):
                    part2[j] = re.sub('\n', '', part2[j])
                    part2[j] = part2[j].strip()
                part1.append(part2)

                certs_UC_str = ""
                certs_CDP_str = ""
                certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                part1.append(certs_UC_str)
                part1.append(certs_CDP_str)
                m.append(part1)
            else:
                lists[i] = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'Хэш SHA1.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?\n',
                    output, re.MULTILINE + re.DOTALL)
                m.append(lists[i][0])
            counter += 1
    elif versiontuple(get_cspversion()[2]) == versiontuple("5.0.11455"):
        lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
        m = []
        counter = 1
        for i in range(1, len(lists), 2):
            lists[i] = f"{counter}-------\n" + lists[i]
            if 'Extended Key Usage' in lists[i]:
                part1 = re.findall(
                    r'(\d+)-{7}\n'
                    r'Issuer.*?: (.+?)\n.*?'
                    r'Subject.*?: (.+?)\n.*?'
                    r'Serial.*?: (0x\w+?)\n'
                    r'SHA1 Hash.*?(\w+?)\n.*?'
                    r'SubjKeyID.*?: (.+?)\n.*?'
                    r'Not valid before.*?(\d.+?)UTC\n'
                    r'Not valid after.*?(\d.+?)UTC.+?\n',
                    lists[i], re.MULTILINE + re.DOTALL)
                part1 = list(part1[0])
                part2 = re.split(r'Extended Key Usage', lists[i], re.MULTILINE + re.DOTALL)[1:]
                part2 = [x for x in part2 if x != ''][0]
                if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                    part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)[:-1]
                    part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                else:
                    part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                for j in range(0, len(part2)):
                    part2[j] = re.sub('\n', '', part2[j])
                    part2[j] = part2[j].strip()
                part1.append(part2)

                certs_UC_str = ""
                certs_CDP_str = ""
                certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                part1.append(certs_UC_str)
                part1.append(certs_CDP_str)
                m.append(part1)
            else:
                lists[i] = re.findall(
                    r'(\d+)-{7}\n'
                    r'Issuer.*?: (.+?)\n.*?'
                    r'Subject.*?: (.+?)\n.*?'
                    r'Serial.*?: (0x\w+?)\n'
                    r'SHA1 Hash.*?(\w+?)\n.*?'
                    r'SubjKeyID.*?: (.+?)\n.*?'
                    r'Not valid before.*?(\d.+?)UTC\n'
                    r'Not valid after.*?(\d.+?)UTC.+?\n',
                    lists[i], re.MULTILINE + re.DOTALL)
                m.append(lists[i][0])
            counter += 1
    elif versiontuple(get_cspversion()[2]) >= versiontuple("4.0.9971"):
        lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
        m = []
        counter = 1
        for i in range(1, len(lists), 2):
            lists[i] = f"{counter}-------\n" + lists[i]
            if 'Назначение/EKU' in lists[i]:
                part1 = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'Хэш SHA1.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?\n',
                    output, re.MULTILINE + re.DOTALL)
                part1 = list(part1[0])
                part2 = re.split(r'Назначение\/EKU', lists[i], re.MULTILINE + re.DOTALL)[1:]
                part2 = [x for x in part2 if x != ''][0]
                if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                    part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)
                    part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                else:
                    part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                for j in range(0, len(part2)):
                    part2[j] = re.sub('\n', '', part2[j])
                    part2[j] = part2[j].strip()
                part1.append(part2)

                certs_UC_str = ""
                certs_CDP_str = ""
                certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                part1.append(certs_UC_str)
                part1.append(certs_CDP_str)
                m.append(part1)
            else:
                lists[i] = re.findall(
                    r'(\d+)-{7}\n'
                    r'Издатель.*?: (.+?)\n.*?'
                    r'Субъект.*?: (.+?)\n.*?'
                    r'Серийный номер.*?: (0x\w+?)\n'
                    r'Хэш SHA1.*?(\w+?)\n.*?'
                    r'Идентификатор ключа.*?: (.+?)\n.*?'
                    r'Выдан.*?(\d.+?)UTC\n'
                    r'Истекает.*?(\d.+?)UTC.+?\n',
                    output, re.MULTILINE + re.DOTALL)
                m.append(lists[i][0])
            counter += 1
    else:
        lists = re.split(r'(\d+)-{7}\n', output, re.MULTILINE + re.DOTALL)[1:]
        m = []
        counter = 1
        for i in range(1, len(lists), 2):
            lists[i] = f"{counter}-------\n" + lists[i]
            if 'Extended Key Usage' in lists[i]:
                part1 = re.findall(
                    r'(\d+)-{7}\n'
                    r'Issuer.*?: (.+?)\n.*?'
                    r'Subject.*?: (.+?)\n.*?'
                    r'Serial.*?: (0x\w+?)\n'
                    r'SHA1 Hash.*?(\w+?)\n.*?'
                    r'SubjKeyID.*?: (.+?)\n.*?'
                    r'Not valid before.*?(\d.+?)UTC\n'
                    r'Not valid after.*?(\d.+?)UTC.+?\n',
                    lists[i], re.MULTILINE + re.DOTALL)
                part1 = list(part1[0])
                part2 = re.split(r'Extended Key Usage', lists[i], re.MULTILINE + re.DOTALL)[1:]
                part2 = [x for x in part2 if x != ''][0]
                if re.findall(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL):
                    part2 = re.split(r'\n\=*\n', part2, re.MULTILINE + re.DOTALL)[:-1]
                    part2 = re.findall(r'[\d+\.]+', part2[0], re.MULTILINE + re.DOTALL)
                else:
                    part2 = re.findall(r'[\d+\.]+', part2, re.MULTILINE + re.DOTALL)
                for j in range(0, len(part2)):
                    part2[j] = re.sub('\n', '', part2[j])
                    part2[j] = part2[j].strip()
                part1.append(part2)

                certs_UC_str = ""
                certs_CDP_str = ""
                certs_UC_str, certs_CDP_str = get_UC_CDP(lists[i])
                part1.append(certs_UC_str)
                part1.append(certs_CDP_str)
                m.append(part1)
            else:
                lists[i] = re.findall(
                    r'(\d+)-{7}\n'
                    r'Issuer.*?: (.+?)\n.*?'
                    r'Subject.*?: (.+?)\n.*?'
                    r'Serial.*?: (0x\w+?)\n'
                    r'SHA1 Hash.*?(\w+?)\n.*?'
                    r'SubjKeyID.*?: (.+?)\n.*?'
                    r'Not valid before.*?(\d.+?)UTC\n'
                    r'Not valid after.*?(\d.+?)UTC.+?\n',
                    lists[i], re.MULTILINE + re.DOTALL)
                m.append(lists[i][0])
            counter += 1
    return m


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


class MainMenu(Gtk.MenuBar):
    def __init__(self):
        super(MainMenu, self).__init__()

        file_menu = Gtk.Menu()

        file_item = Gtk.MenuItem(label="_Операции", use_underline=True)
        file_item.set_submenu(file_menu)

        file_menu_license = Gtk.Menu()
        file_item_license = Gtk.MenuItem(label="_Лицензия", use_underline=True)
        file_item_license.set_submenu(file_menu_license)
        self.add_license = Gtk.MenuItem(label="_Ввод лицензии КриптоПро CSP", use_underline=True)
        self.view_license = Gtk.MenuItem(label="_Просмотр лицензии КриптоПро CSP", use_underline=True)

        file_menu_operations_certs = Gtk.Menu()
        file_item_operations_certs = Gtk.MenuItem(label="_Сертификаты", use_underline=True)
        file_item_operations_certs.set_submenu(file_menu_operations_certs)

        self.install_root_certs = Gtk.MenuItem(label="_Установка корневых сертификатов", use_underline=True)
        self.install_crl = Gtk.MenuItem(label="_Установка списков отозванных сертификатов", use_underline=True)
        self.write_cert_to_cont = Gtk.MenuItem(label="_Запись сертификата в контейнер", use_underline=True)
        self.export_cont_cert = Gtk.MenuItem(label="_Экспортировать сертификат из контейнера", use_underline=True)
        self.choose_local_cert_for_cont = Gtk.MenuItem(label="Связать сертификат с контейнером", use_underline=True)

        file_menu_operations_conts = Gtk.Menu()
        file_item_operations_conts = Gtk.MenuItem(label="_Контейнеры", use_underline=True)
        file_item_operations_conts.set_submenu(file_menu_operations_conts)

        self.view_root = Gtk.MenuItem(label="_Просмотр корневых сертификатов", use_underline=True)
        self.view_crl = Gtk.MenuItem(label="_Просмотр списков отозванных сертификатов", use_underline=True)
        self.usb_flash_container = Gtk.MenuItem(label="_Скопировать контейнер с usb-flash накопителя",
                                                use_underline=True)
        self.token_container = Gtk.MenuItem(label="_Скопировать контейнер с токена", use_underline=True)
        self.hdimage_container = Gtk.MenuItem(label="_Скопировать контейнер из HDIMAGE на токен", use_underline=True)

        file_item.set_submenu(file_menu)
        file_menu.append(file_item_license)
        file_menu_license.append(self.add_license)
        file_menu_license.append(self.view_license)
        file_menu.append(Gtk.SeparatorMenuItem.new())

        file_menu.append(file_item_operations_certs)
        file_menu_operations_certs.append(self.install_root_certs)
        file_menu_operations_certs.append(self.install_crl)
        file_menu_operations_certs.append(self.write_cert_to_cont)
        file_menu_operations_certs.append(self.export_cont_cert)
        file_menu_operations_certs.append(self.choose_local_cert_for_cont)
        file_menu_operations_certs.append(Gtk.SeparatorMenuItem.new())
        file_menu_operations_certs.append(self.view_root)
        file_menu_operations_certs.append(self.view_crl)
        file_menu.append(Gtk.SeparatorMenuItem.new())

        file_menu.append(file_item_operations_conts)
        file_menu_operations_conts.append(self.token_container)
        file_menu_operations_conts.append(self.usb_flash_container)
        file_menu_operations_conts.append(self.hdimage_container)
        self.append(file_item)

        Usefull_menu = Gtk.Menu()
        Usefull_menu_item = Gtk.MenuItem(label="_Полезные ссылки", use_underline=True)
        Usefull_menu_item.set_submenu(Usefull_menu)
        self.actionUsefull_install = Gtk.MenuItem(label="_Установка КриптоПро CSP", use_underline=True)
        Usefull_menu.append(self.actionUsefull_install)
        self.actionUsefull_commands = Gtk.MenuItem(label="_Работа с сертификатами КриптоПро CSP", use_underline=True)
        Usefull_menu.append(self.actionUsefull_commands)
        self.append(Usefull_menu_item)

        About_menu = Gtk.Menu()
        About_menu_item = Gtk.MenuItem(label="_О программе", use_underline=True)
        About_menu_item.set_submenu(About_menu)
        self.actionAbout = Gtk.MenuItem(label="_О программе", use_underline=True)
        About_menu.append(self.actionAbout)
        self.append(About_menu_item)


class TokenUI(Gtk.Box):
    def __init__(self, parent, isApp):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.__parent = parent
        global modules_list
        self.set_size_request(500, 388)

        self.info_class = InfoClass()
        if not os.path.exists('/opt/cprocsp/bin/%s/certmgr' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/cryptcp' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/list_pcsc' % arch) \
                or not os.path.exists('/opt/cprocsp/bin/%s/csptest' % arch) \
                or not os.path.exists('/opt/cprocsp/sbin/%s/cpconfig' % arch):
            self.info_class.print_simple_info(
                f'СКЗИ Крипто Про CSP или некоторые его компоненты не установлены для {arch}.')
            # raise Exception(f'СКЗИ Крипто Про CSP или некоторые его компоненты не установлены для {arch}.')
            exit(-1)

        if versiontuple("4.0.0") < versiontuple(get_cspversion()[2]) < versiontuple("5.0.0"):
            if versiontuple(get_cspversion()[2]) < versiontuple("4.0.9708"):
                self.info_class.print_simple_info('Текущая версия СКЗИ Крипто Про CSP не поддерживается.')
                # raise Exception('Текущая версия СКЗИ Крипто Про CSP не поддерживается.')
                exit(-1)
        elif versiontuple(get_cspversion()[2]) > versiontuple("5.0.0"):
            if versiontuple(get_cspversion()[2]) < versiontuple("5.0.11455"):
                self.info_class.print_simple_info('Текущая версия СКЗИ Крипто Про CSP не поддерживается.')
                # raise Exception('Текущая версия СКЗИ Крипто Про CSP не поддерживается.')
                exit(-1)

        if not os.popen("systemctl list-unit-files | grep enabled | grep pcscd").readlines():
            os.system("systemctl enable --now pcscd")

        self.main_menu = MainMenu()
        self.main_menu.add_license.connect("activate", self.info_class.enter_license)
        self.main_menu.view_license.connect("activate", self.view_license)
        self.main_menu.install_root_certs.connect("activate", self.info_class.open_root_certs)
        self.main_menu.install_crl.connect("activate", self.info_class.open_crl)
        self.main_menu.view_root.connect("activate", self.view_root)
        self.main_menu.view_crl.connect("activate", self.view_crl)
        self.main_menu.write_cert_to_cont.connect("activate", self.write_cert)
        self.main_menu.export_cont_cert.connect("activate", self.export_container_cert)
        self.main_menu.choose_local_cert_for_cont.connect("activate", self.info_class.install_local_cert_to_container)
        self.main_menu.actionAbout.connect("activate", self.about_iterate_self)
        self.main_menu.actionUsefull_install.connect("activate", self.usefull_install)
        self.main_menu.actionUsefull_commands.connect("activate", self.usefull_commands)
        self.main_menu.token_container.connect("activate", self.token_container_install)
        self.main_menu.usb_flash_container.connect("activate", self.usb_flash_container_install)
        self.main_menu.hdimage_container.connect("activate", self.hdimage_container_install)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_border_width(3)
        self.main_box.pack_start(self.main_menu, False, True, 0)

        # box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # self.token_refresh.connect("clicked", self.refresh_token)
        # box.pack_start(self.arch_label, False, False, 0)
        # self.main_box.pack_start(box, False, False, 3)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.token_refresh = Gtk.Button.new_with_label("Обновить")
        self.token_refresh.connect("clicked", self.refresh_token)
        box.pack_end(self.token_refresh, True, True, 0)
        self.main_box.pack_start(box, False, False, 0)

        scroll_window = Gtk.ScrolledWindow()
        box = Gtk.Frame()

        scroll_window.add(box)
        scroll_window.set_size_request(200, 150)
        self.token_list = Gtk.ListStore(str, str, str, bool)
        self.treeview = Gtk.TreeView(model=self.token_list)
        self.treeview.get_selection().connect("changed", self.select_token)

        px_renderer = Gtk.CellRendererPixbuf()
        px_column = Gtk.TreeViewColumn('Выберите ключевой носитель или хранилище')
        px_column.pack_start(px_renderer, False)
        str_renderer = Gtk.CellRendererText()
        px_column.pack_start(str_renderer, False)
        # set data connector function/method
        px_column.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        px_column.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        self.treeview.append_column(px_column)

        box.add(self.treeview)
        self.main_box.pack_start(scroll_window, True, True, 7)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # self.asReader = Gtk.Button.new_with_label("Подключить как считыватель")
        # self.asReader.connect("clicked", self.set_reader)
        # self.asReader.set_sensitive(False)
        # box.pack_start(self.asReader, True, True, 0)

        self.cachePIN = Gtk.Button.new_with_label("Сохранить PIN")
        self.cachePIN.set_sensitive(False)
        self.cachePIN.connect("clicked", self.cache_pin)
        box.pack_start(self.cachePIN, True, True, 3)

        self.changePIN = Gtk.Button.new_with_label("Изменить PIN")
        self.changePIN.set_sensitive(False)
        self.changePIN.connect("clicked", self.change_pin)
        box.pack_start(self.changePIN, True, True, 3)
        self.main_box.pack_start(box, False, False, 0)
        scroll_window = Gtk.ScrolledWindow()
        box = Gtk.Frame()

        scroll_window.add(box)
        scroll_window.set_size_request(200, 150)


        # NEW model structure = {cert_index: type str, cert_item:, SubjKeyID: type str, color: type Gdk.RGBA}
        self.cert_list = Gtk.ListStore(str, str, str, Gdk.RGBA)
        # self.cert_list = Gtk.ListStore(str, str, Gdk.RGBA)
        self.treeview_cert = Gtk.TreeView(model=self.cert_list)

        cell = Gtk.CellRendererText()
        self.treeview_cert_col = Gtk.TreeViewColumn("Выберите контейнер сертификата", cell, text=1, background_rgba=3)
        self.treeview_cert.append_column(self.treeview_cert_col)
        self.treeview_cert.get_selection().connect("changed", self.select_cert)

        box.add(self.treeview_cert)
        self.main_box.pack_start(scroll_window, True, True, 7)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.cert_delete = Gtk.Button.new_with_label("Удалить")
        self.cert_delete.set_sensitive(False)
        self.cert_delete.connect("clicked", self.delete_cert)
        box.pack_start(self.cert_delete, True, True, 0)

        self.cert_view = Gtk.Button.new_with_label("Просмотр")
        self.cert_view.set_sensitive(False)

        box.pack_start(self.cert_view, True, True, 7)
        self.handler_id_install = ""
        self.handler_id_view_cert = ""
        self.cert_install = Gtk.Button.new_with_label("Установить")
        self.cert_install.set_sensitive(False)

        box.pack_start(self.cert_install, True,
                       True, 0)
        self.main_box.pack_start(box, False, False, 0)

        self.token_refresh.clicked()
        self.pack_start(self.main_box, True, True, 0)

    ############################################################################################
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
                self.treeview_cert_col.set_title('Выберите контейнер сертификата')
                # self.asReader.set_sensitive(True)
                self.token = temp[1]
                certs = get_token_certs(str(self.token))[0]
                counter = 0
                for cert in certs:
                    cert_item = cert.split('|')[0].split('\\')[-1]
                    self.cert_list.append([str(counter), cert_item, "", Gdk.RGBA(red=0, green=0, blue=0, alpha=0)])
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
                self.treeview_cert_col.set_title("Выберите сертификат")
                certs = get_store_certs(model.get_value(iter, 2))
                for cert in certs:
                    self.cert_index = cert[0]
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                    if datetime.strptime(cert[6], '%d/%m/%Y  %H:%M:%S ') < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                    try:
                        cert_subject_cn = dict(re.findall(
                            '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)',
                            cert[2], re.UNICODE))
                        cert_subject_cn = cert_subject_cn['CN'] if 'CN' in cert_subject_cn else ""
                        cert_subject_o = dict(re.findall(
                            '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)',
                            cert[2], re.UNICODE))
                        cert_subject_o = cert_subject_o['O'] if 'O' in cert_subject_o else cert_subject_o['CN']
                        cert_issuer_cn = dict(re.findall(
                            '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)',
                            cert[1], re.UNICODE))
                        cert_issuer_cn = cert_issuer_cn['CN'] if 'CN' in cert_issuer_cn else ""

                        cert_item = "%s\nвыдан %s\nорганизация %s" % (cert_subject_cn, cert_issuer_cn, cert_subject_o)

                        cert_ID = cert[5]

                        self.cert_list.append([self.cert_index, cert_item, cert_ID, color, ])
                    except KeyError as e:
                        print(f" Couldn't parse {e}")
        return True

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
                        win.print_simple_info(f"Выбрано {selected} контейнера(ов),\n"
                                              "пожалуйста выберите лишь 1")
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
                                if output == "success":
                                    flag_success = True
                                elif output == "Операция отменена пользователем":
                                    flag_cancel = True
                                if flag_success:
                                    win.print_simple_info("Сертификат успешно скопирован в контейнер")
                                elif flag_cancel:
                                    win.print_simple_info("Операция отменена пользователем")
                                else:
                                    win.print_big_error(output, 500, 300)
                else:
                    win.print_simple_info("Операция отменена пользователем")
            else:
                win.print_simple_info("Токены не обнаружены")
        else:
            win.print_simple_info("Токены не обнаружены")

    def delete_cert(self, button):
        (model, iter) = self.cert_selection.get_selected()
        if self.isToken:
            if self.info_class.delete_from_Token() == Gtk.ResponseType.OK:
                ret = del_cont(self.cert)
                if ret == u"Сертификат успешно удален":
                    self.info_class.print_simple_info(ret)
                    self.cert_list.remove(iter)
                    self.cert_selection.unselect_all()
                else:
                    self.info_class.print_info(ret)

                self.cert_delete.set_sensitive(False)
                self.cert_view.set_sensitive(False)
                self.cert_install.set_sensitive(False)
        else:
            if self.info_class.delete_from_nonToken() == Gtk.ResponseType.OK:
                ret = del_store_cert(self.store, self.certID)
                if ret == u"Сертификат успешно удален":
                    self.info_class.print_simple_info(ret)
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

            cert_index = model.get_value(iter, 0)
            line = cert_info[int(cert_index) - 1]
        if line:
            cert_view = ViewCert()
            cert_view.set_model(Gtk.ListStore(str, Gdk.RGBA), True)
            color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
            cert_view.set_title("Просмотр")
            item = "<b>Эмитент</b>"
            cert_view.cert_listview.append([item, color])
            issuer_info = dict(re.findall(
                '([A-Za-z0-9\.]+?)=([\xab\xbb\(\)\w \.\,0-9@\-\#\/\"\/\']+|\"(?:\\.|[^\"])*\")(?:, |$)', line[1],
                re.UNICODE))
            for field in issuer_info:
                item = '<b>%s</b>: %s' % (translate_cert_fields(field), issuer_info[field])
                cert_view.cert_listview.append([item, color])
            item = '<b>Субъект</b>:'
            cert_view.cert_listview.append([item, color])
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
                cert_view.cert_listview.append([item, color])
            cert_serial = line[3][2:]
            item = '<b>Серийный номер</b>: %s' % cert_serial
            cert_view.cert_listview.append([item, color])
            not_valid_before = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
            item = '<b>Не действителен до</b>: %s' % datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S')
            cert_view.cert_listview.append([item, color])
            not_valid_after = datetime.strptime(line[7], '%d/%m/%Y  %H:%M:%S ')
            color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)  # transparent to apply system colors
            if not_valid_after < datetime.utcnow():
                color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
            item = '<b>Не действителен после</b>: %s' % datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S')
            cert_view.cert_listview.append([item, color])
            item = '<b>Расширенное использование ключа</b>: '
            cert_view.cert_listview.append([item, color])
            try:
                if type(line[8]) == str:
                    lines = line[8].split('\n')
                    for i in range(0, len(lines)):
                        lines[i] = lines[i].strip()
                    ext_key = lines
                elif type(line[8]) == list:
                    ext_key = line[8]
            except IndexError:
                ext_key = ['<i>Не имеет</i>']
            for oid in ext_key:
                item = translate_cert_fields(oid)
                cert_view.cert_listview.append([item, color])
            try:
                if type(line[9]) == str and len(line[9]) > 0:
                    item = '<b>Необходимые корневые сертификаты</b>: '
                    cert_view.cert_listview.append([item, color])
                    for l in line[9].split("\n"):
                        cert_view.cert_listview.append([l, color])
                    self.CA_LIST_STR = line[9]
            except IndexError:
                pass
            try:
                if type(line[10]) == str and len(line[10]) > 0:
                    item = '<b>Необходимые промежуточные сертификаты</b>: '
                    cert_view.cert_listview.append([item, color])
                    for l in line[10].split("\n"):
                        cert_view.cert_listview.append([l, color])
                    self.CDP_LIST_STR = line[10]
            except IndexError:
                pass
            cert_view.connect("destroy", Gtk.main_quit)
            cert_view.show_all()
            Gtk.main()
        else:
            win = InfoClass()
            win.print_error("Открытая часть сертификата не обнаружена")

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
        license_view.set_model(Gtk.ListStore(str), False)
        item = license_info.decode("utf-8")
        license_view.cert_listview.append([item])
        license_view.set_title("Просмотр лицензий КриптоПро CSP")
        license_view.connect("destroy", Gtk.main_quit)
        license_view.show_all()
        Gtk.main()

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
                                if dest_stores != '<ключевых носителей не обнаружено>':
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
                                            win.print_error("Необходимо выбрать 1 хранилище\n"
                                                            "для завершения экспортирования")
                                        elif selected_stores == 1:
                                            output = os.popen(
                                                f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{selected_store_hdimage}' "
                                                f"-contdest '\\\\.\\{selected_store}\\{container_name}'").readlines()

                                            if not win.install_cert_from_or_to_container(
                                                    f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                win.print_simple_info("Операция отменена пользователем")
                                    else:
                                        win.print_simple_info("Операция отменена пользователем")
                                else:
                                    win.print_error("Токены не обнаружены")
                            elif out_name == "canceled":
                                win.print_simple_info("Операция отменена пользователем")
                            elif out_name == "empty":
                                win.print_error("Не введено имя")
                        else:
                            win.print_error("Пожалуйста, выберите только 1 контейнер")
                    else:
                        win.print_error("Не выбрано контейнеров")
                else:
                    win.print_simple_info("Операция отменена пользователем")
            else:
                win.print_error("Хранилища в hdimage не обнаружены")

        else:
            win.print_simple_info("Операция отменена пользователем")

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
                                        win.print_simple_info("Сертификат успешно экспортирован")
                                    else:
                                        win.print_big_error(output, 500, 300)
                                else:
                                    win.print_simple_info("Операция отменена пользователем")
                            elif out_name == "canceled":
                                win.print_simple_info("Операция отменена пользователем")
                            elif out_name == "empty":
                                win.print_error("Не введено имя")
                        else:
                            win.print_error("Пожалуйста, выберите только 1 контейнер")
                    else:
                        win.print_error("Не выбрано контейнеров")
                else:
                    win.print_simple_info("Операция отменена пользователем")
            else:
                win.print_error("Хранилища не обнаружены")
        else:
            win.print_simple_info("Операция отменена пользователем")

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
                            win.print_simple_info(f"Выбрано {selected} контейнера(ов),\n"
                                                  f"приготовьтесь ввести пароли контейнеров\nнесколько раз и выбрать "
                                                  f"сертификаты\nоткрытой части ключа\n"
                                                  f"(если они не установятся автоматически)")
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
                                            win.print_error("Необходимо выбрать 1 хранилище\n"
                                                            "для завершения экспортирования")
                                        elif selected_stores == 1:
                                            output = os.popen(
                                                f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{cont[0]}' "
                                                f"-contdest '\\\\.\\{selected_store}\\{container_name}' | iconv -f cp1251").readlines()

                                            if not win.install_cert_from_or_to_container(
                                                    f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                win.print_simple_info("Операция отменена пользователем")
                                    else:
                                        win.print_simple_info("Операция отменена пользователем")
                                elif out_name == "canceled":
                                    win.print_simple_info("Операция отменена пользователем")
                                elif out_name == "empty":
                                    win.print_error("Не введено имя")
                    else:
                        win.print_simple_info("Операция отменена пользователем")
                else:
                    win.print_simple_info("Токены не обнаружены")
            else:
                win.print_simple_info("Токены не обнаружены")
        else:
            win.print_simple_info("Операция отменена пользователем")

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
                                win.print_simple_info(f"Выбрано {len(selected_containers)} контейнера(ов),\n"
                                                      f"приготовьтесь ввести пароли контейнеров\nнесколько раз и выбрать "
                                                      f"сертификаты\nоткрытой части ключа\n(если они не "
                                                      f"установятся автоматически)")
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
                                                win.print_error("Необходимо выбрать 1 хранилище\n"
                                                                "для завершения экспортирования")
                                            elif selected_stores == 1:
                                                output = os.popen(
                                                    f"/opt/cprocsp/bin/{arch}/csptest -keycopy -contsrc '{cont[0]}' "
                                                    f"-contdest '\\\\.\\{selected_store}\\{container_name}' | iconv -f cp1251").readlines()

                                                if not win.install_cert_from_or_to_container(
                                                        f"\\\\.\\{selected_store}\\{container_name}", selected_store):
                                                    win.print_simple_info("Операция отменена пользователем")
                                        else:
                                            win.print_simple_info("Операция отменена пользователем")
                                    elif out_name == "canceled":
                                        win.print_simple_info("Операция отменена пользователем")
                                    elif out_name == "empty":
                                        win.print_error("Не введено имя")
                                else:
                                    win.print_simple_info("Выбран не верный путь, отмена операции")
            else:
                win.print_simple_info("Операция отменена пользователем")
        else:
            win.print_simple_info("Не обнаружено контейнеров,\nотносящихся к usb-flash накопителю")

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
                    win.print_simple_info("Переподключите usb-flash накопитель\nи повторите операцию")
                elif status == "canceled":
                    win.print_simple_info("Операция отменена пользователем")
            else:
                self.call_flash_container_install(False)
        else:
            win.print_simple_info("Операция отменена пользователем")

    def install_cert(self, widget):
        win = InfoClass()
        ###
        # Проверка на наличие домена, если он есть, то включаем правило для secretnet
        # правило единое для всех доменных пользователей
        ###
        global appdir
        domain_info = os.popen(f"{appdir}/usr/sbin/realm list").readlines() if appdir else os.popen("/usr/sbin/realm list").readlines()
        if domain_info:
            status = self.info_class.call_secretnet_configs("доменных пользователей", "domain")
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
                        self.info_class.print_simple_info(
                            u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                            strk_out.append("Успешно установлены корневые сертификаты:")
                            for succ in success_ca:
                                strk_out.append(f"{succ}")

                        if len(success_cdp) > 0:
                            if len(success_ca) > 0:
                                strk_out += "\n"
                            strk_out.append("Успешно установлены сертификаты отзыва:")
                            for succ in success_cdp:
                                strk_out.append(f"{succ}")

                        if len(errors_ca) > 0:
                            if len(success_ca) > 0 or len(success_cdp) > 0:
                                strk_out += "\n"
                            strk_out.append("Ошибка при установке корневых сертификатов:")
                            for err in errors_ca:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        if len(errors_cdp) > 0:
                            strk_out.append("Ошибка при установке сертификатов отзыва:")
                            for err in errors_cdp:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        view = ViewCertOutput()
                        view.set_model(strk_out)
                        view.connect("destroy", Gtk.main_quit)
                        view.show_all()
                        Gtk.main()
                else:
                    # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
                    output = win.choose_open_cert_to_close_container(self.cert)
                    if not output[0]:
                        strk = ""
                        for line in output[1]:
                            strk += line
                        self.info_class.print_error(strk)
            elif status == "just_installed":
                win.print_simple_info("Переподключите usb-flash накопитель\nи повторите операцию")
            elif status == "canceled":
                win.print_simple_info("Операция отменена пользователем")
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
                    self.info_class.print_simple_info(
                        u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                        strk_out.append("Успешно установлены корневые сертификаты:")
                        for succ in success_ca:
                            strk_out.append(f"{succ}")

                    if len(success_cdp) > 0:
                        strk_out.append("Успешно установлены сертификаты отзыва:")
                        for succ in success_cdp:
                            strk_out.append(f"{succ}")

                    if len(errors_ca) > 0:
                        strk_out.append("Ошибка при установке корневых сертификатов:")
                        for err in errors_ca:
                            strk_out.append(f"{err[0]}\n{err[1]}")

                    if len(errors_cdp) > 0:
                        strk_out.append("Ошибка при установке сертификатов отзыва:")
                        for err in errors_cdp:
                            strk_out.append(f"{err[0]}\n{err[1]}")

                    view = ViewCertOutput()
                    view.set_model(strk_out)
                    view.connect("destroy", Gtk.main_quit)
                    view.show_all()
                    Gtk.main()
                else:
                    self.info_class.print_simple_info(u"Сертификат успешно установлен.")
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
        root_view = ListCert(root_info, True)
        root_view.connect("destroy", Gtk.main_quit)
        root_view.set_title("Корневые сертификаты")
        root_view.set_model(Gtk.ListStore(str, str, str, Gdk.RGBA), True)
        Gtk.main()

    def view_crl(self, widget):
        crl_info = list_crls()
        crl_view = ListCert(crl_info, False)
        crl_view.connect("destroy", Gtk.main_quit)
        crl_view.set_title("Отозванные сертификаты")
        crl_view.set_model(Gtk.ListStore(str, str, Gdk.RGBA), True)
        Gtk.main()

    def about_iterate_self(self, widget):
        about = About()
        about.set_title("О программе")
        about.connect("destroy", Gtk.main_quit)
        about.show_all()
        Gtk.main()

    def usefull_install(self, widget):
        webbrowser.open_new_tab("https://redos.red-soft.ru/base/other-soft/szi/cryptopro-4/")

    def usefull_commands(self, widget):
        webbrowser.open_new_tab("https://redos.red-soft.ru/base/other-soft/szi/certs-cryptopro/")

    def refresh_token(self, button):
        self.token_list.clear()
        if hasattr(self, 'cert_selection'):
            self.cert_selection.unselect_all()
        tokens = get_tokens()
        root_store_item = TokenListItem()
        root_store_item.text = "Хранилище корневых сертификатов"
        root_store_item.isToken = False
        root_store_item.storage = 'uRoot'
        root_store_item.icon = 'root'
        self.token_list.append(
            [root_store_item.icon, root_store_item.text, root_store_item.storage, root_store_item.isToken])

        personal_store_item = TokenListItem()
        personal_store_item.text = "Личное хранилище сертификатов"
        personal_store_item.isToken = False
        personal_store_item.storage = 'uMy'
        personal_store_item.icon = "personal"
        self.token_list.append([personal_store_item.icon, personal_store_item.text, personal_store_item.storage,
                                personal_store_item.isToken])
        if tokens[1]:
            self.token_item = TokenListItem()
            self.token_item.text = '<Ключевых носителей не обнаружено>'
        else:
            self.tokens_for_import_container = Gtk.ListStore(str, bool)
            for token in tokens[0]:
                token_item = TokenListItem()
                token_item.token_name = token
                token_item.text = ('%s - сер. № %s' % (token, self.get_token_serial(token)))
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

    def set_reader(self, button):
        if self.set_as_reader(self.token):
            self.info_class.print_simple_info("Ключевой носитель %s успешно добавлен в качестве "
                                              "считывателя" % self.token_name)
        else:
            self.info_class.print_simple_info("Произошла ошибка")

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
                self.info_class.print_simple_info("Пин код успешно изменен")

    def cache_pin(self, button):
        result = self.info_class.cache_pin()
        if (result[0] == Gtk.ResponseType.OK) and (result[1] != ''):
            if not self.add_ini(result[1], self.cont_id):
                self.info_class.print_simple_info("PIN-код успешно сохранен")

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


class About(Gtk.Window):
    def __init__(self):
        super(About, self).__init__()
        self.set_keep_above(True)
        self.set_border_width(5)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        button = Gtk.Button.new_with_label("X")
        button.connect("clicked", self.button_close_clicked)
        hb.pack_end(button)
        self.set_titlebar(hb)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        global appdir
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            filename=f"{appdir}/usr/share/icons/hicolor/64x64/apps/token-manager.png"
            ) if appdir else GdkPixbuf.Pixbuf.new_from_file(
            filename="/usr/share/icons/hicolor/64x64/apps/token-manager.png"
            )


        self.image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.box.pack_start(self.image, False, False, 0)
        self.label = Gtk.Label()
        self.label.set_markup(f"<b>token-manager {VERSION}</b>\n"
                              "Версия CSP: %s\n"
                              "Класс криптосредств: %s\n"
                              "Релиз: %s "
                              "ОС: %s" % get_cspversion())
        self.label_href = Gtk.Label()
        self.label_href.set_markup("\n"
                                   "Борис Макаренко УИТ ФССП России"
                                   "\nE-mail: <a href='mailto:makarenko@fssprus.ru'>makarenko@fssprus.ru</a>"
                                   "\n<a href='mailto:bmakarenko90@gmail.com'>bmakarenko90@gmail.com</a>\n"
                                   "-----------------------------\n"
                                   "Владлен Мурылев ООО \"РЕД СОФТ\""
                                   "\nE-mail: <a href='mailto:vladlen.murylyov@red-soft.ru'>vladlen.murylyov@red-soft.ru</a>"
                                   "\n-----------------------------"
                                   "\n\t\t<a href='http://opensource.org/licenses/MIT'>Лицензия MIT</a>")
        self.box.pack_start(self.label, True, True, 0)
        self.main_box.pack_start(self.box, True, True, 0)
        self.main_box.pack_end(self.label_href, False, False, 0)
        self.add(self.main_box)

    def button_close_clicked(self, button):
        self.destroy()


class ListCert(Gtk.ApplicationWindow):
    list_data = []
    is_root = False

    def __init__(self, certlist_data, is_root):
        super(ListCert, self).__init__()
        self.set_border_width(5)
        self.set_keep_above(True)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        button = Gtk.Button.new_with_label("X")
        button.connect("clicked", self.button_close_clicked)
        hb.pack_end(button)
        self.set_titlebar(hb)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_skip_taskbar_hint(True)
        self.list_data = certlist_data
        self.is_root = is_root

    def button_close_clicked(self, button):
        self.destroy()

    def set_model(self, model, with_color):
        self.token_list = model
        self.filter = self.token_list.filter_new()
        self.filter.set_visible_func(self.visible_cb)
        self.view = Gtk.TreeView(model=self.filter)
        cell = Gtk.CellRendererText()

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type to filter...")
        self.entry.connect("changed", self.refresh_filter)
        self.main_box.pack_start(self.entry, False, False, 0)

        if self.is_root:
            self.set_size_request(1270, 500)
            col1 = Gtk.TreeViewColumn("Эмитент", cell, text=0, background_rgba=3)
            col2 = Gtk.TreeViewColumn("Субъект", cell, text=1, background_rgba=3)
            col3 = Gtk.TreeViewColumn("Основная информация", cell, text=2, background_rgba=3)

            self.view.append_column(col1)
            self.view.append_column(col2)
            self.view.append_column(col3)

            for line in self.list_data:
                not_valid_before = datetime.strptime(line[5], '%d/%m/%Y  %H:%M:%S ')
                not_valid_after = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
                color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                if not_valid_after < datetime.utcnow():
                    color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
                    item = ('Серийный номер: %s\nSHA1 отпечаток: %s\nНе действителен до: %s\n'
                            'Не действителен после: %s' % (line[3], line[4],
                                                           datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S'),
                                                           datetime.strftime(not_valid_after,
                                                                             '%d.%m.%Y %H:%M:%S')))
                else:
                    item = ('Серийный номер: %s\nХэш SHA1: %s\nНе действителен до: %s\n'
                            'Не действителен после: %s' % (line[3], line[4],
                                                           datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S'),
                                                           datetime.strftime(not_valid_after,
                                                                             '%d.%m.%Y %H:%M:%S')))
                self.token_list.append([line[1], line[2], item, color])
        else:
            self.set_default_size(800, 343)
            col1 = Gtk.TreeViewColumn("Субъект", cell, text=0, background_rgba=2)
            col2 = Gtk.TreeViewColumn("Даты", cell, text=1, background_rgba=2)

            self.view.append_column(col1)
            self.view.append_column(col2)

            for line in self.list_data:
                this_update = datetime.strptime(line[2], '%d/%m/%Y  %H:%M:%S ')
                next_update = datetime.strptime(line[3], '%d/%m/%Y  %H:%M:%S ')
                color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)

                if next_update < datetime.utcnow():
                    color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                item = ('Дата выпуска: %s UTC\nДата обновления: %s UTC' %
                        (datetime.strftime(this_update, '%d.%m.%Y %H:%M:%S'),
                         datetime.strftime(next_update, '%d.%m.%Y %H:%M:%S')))
                self.token_list.append([line[1], item, color])

        self.sw = Gtk.ScrolledWindow()
        self.sw.add(self.view)
        self.main_box.pack_start(self.sw, True, True, 0)
        self.add(self.main_box)
        self.show_all()

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


class ViewCert(Gtk.ApplicationWindow):
    def __init__(self):
        super(ViewCert, self).__init__()
        self.set_default_size(600, 500)
        self.set_border_width(5)
        self.set_keep_above(True)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        button = Gtk.Button.new_with_label("X")
        button.connect("clicked", self.button_close_clicked)
        hb.pack_end(button)
        self.set_titlebar(hb)
        self.main_box = Gtk.Box()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_skip_taskbar_hint(True)

    def button_close_clicked(self, button):
        self.destroy()

    def set_model(self, model, with_color):
        self.cert_listview = model
        self.view = Gtk.TreeView(model=self.cert_listview)
        cell = Gtk.CellRendererText()
        if with_color:
            col = Gtk.TreeViewColumn("Сертификаты", cell, markup=0, background_rgba=1)
        else:
            col = Gtk.TreeViewColumn("Сертификаты", cell, markup=0)
        cell.set_property("editable", True)
        self.view.append_column(col)
        self.sw = Gtk.ScrolledWindow()
        self.sw.add(self.view)
        self.main_box.pack_start(self.sw, True, True, 0)
        self.add(self.main_box)
        self.show_all()

class ViewCertOutput(Gtk.ApplicationWindow):
    def __init__(self):
        super(ViewCertOutput, self).__init__()
        self.set_default_size(650, 400)
        self.set_border_width(5)
        self.set_keep_above(True)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        button = Gtk.Button.new_with_label("X")
        button.connect("clicked", self.button_close_clicked)
        hb.pack_end(button)
        self.set_titlebar(hb)
        self.main_box = Gtk.Box()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_skip_taskbar_hint(True)


    def set_model(self, info):
        self.liststore = Gtk.ListStore(str)
        for i in info:
            self.liststore.append([i])
        treeview = Gtk.TreeView(model=self.liststore)
        # sel = treeview.get_selection()
        # sel.set_mode(Gtk.SelectionMode.NONE)
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        column_text = Gtk.TreeViewColumn("", renderer_text, text=0)
        treeview.append_column(column_text)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        self.main_box.pack_start(scrolled_tree, True, True, 0)
        self.add(self.main_box)
        self.show_all()

    def button_close_clicked(self, button):
        self.destroy()

class InfoClass(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        # box = Gtk.Box()
        # self.add(box)

    def print_info(self, info, widtn, heigth):
        self.liststore = Gtk.ListStore(str)
        self.liststore.append([info])
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.INFO,
                                         buttons=Gtk.ButtonsType.OK)
        dialogWindow.set_title("Информация")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()
        dialogWindow.set_border_width(2)
        treeview = Gtk.TreeView(model=self.liststore)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("", renderer_text, text=0)
        treeview.append_column(column_text)

        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)

        dialogBox.pack_start(scrolled_tree, True, True, 0)
        dialogWindow.set_size_request(widtn, heigth)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()

    def print_big_error(self, info, widtn, heigth):
        self.liststore = Gtk.ListStore(str)
        self.liststore.append([info])
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.ERROR,
                                         buttons=Gtk.ButtonsType.OK)
        dialogWindow.set_title("Ошибка")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore)
        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("", renderer_text, text=0)
        treeview.append_column(column_text)

        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        dialogWindow.set_size_request(widtn, heigth)
        dialogBox.pack_start(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()

    def print_simple_info(self, info):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK,
                                   text="Информация")
        dialog.format_secondary_text(info)
        dialog.run()
        dialog.destroy()

    def print_error(self, error):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.CANCEL, text="Ошибка")
        dialog.format_secondary_text(error)
        dialog.run()
        dialog.destroy()

    def change_pin(self, text):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text=text)
        dialogWindow.set_title("Ввод PIN-кода")
        dialogBox = dialogWindow.get_content_area()
        pinEntry = Gtk.Entry()
        dialogBox.pack_end(pinEntry, False, False, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        pin = pinEntry.get_text()
        dialogWindow.destroy()
        return [response, pin]

    def cache_pin(self):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text="Ввод PIN-кода")
        dialogWindow.set_title("Введите PIN-код:")
        dialogBox = dialogWindow.get_content_area()
        pinEntry = Gtk.Entry()
        dialogBox.pack_end(pinEntry, False, False, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        pin = pinEntry.get_text()
        dialogWindow.destroy()
        return [response, pin]

    def install_local_cert(self, widget):
        dialog = Gtk.FileChooserDialog(title="Выберите файл(ы)", parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Сертификаты *.cer")
        filter.add_mime_type("Сертификаты")
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            dialog.destroy()
            if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.0"):
                print(versiontuple(get_cspversion()[2]))
                if self.ask_about_mmy(self) == Gtk.ResponseType.OK:
                    store = "mMy"
                else:
                    store = "uMy"
            else:
                store = "uMy"
            ret = inst_cert_from_file(file_name, store)
            if ret == u"Сертификат успешно установлен":
                # self.print_simple_info(ret)
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
                    self.print_simple_info(
                        u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                        strk_out.append("Успешно установлены корневые сертификаты:")
                        for succ in success_ca:
                            strk_out.append(f"{succ}")

                    if len(success_cdp) > 0:
                        strk_out.append("Успешно установлены сертификаты отзыва:")
                        for succ in success_cdp:
                            strk_out.append(f"{succ}")

                    if len(errors_ca) > 0:
                        strk_out.append("Ошибка при установке корневых сертификатов:")
                        for err in errors_ca:
                            strk_out.append(f"{err[0]}\n{err[1]}")

                    if len(errors_cdp) > 0:
                        strk_out.append("Ошибка при установке сертификатов отзыва:")
                        for err in errors_cdp:
                            strk_out.append(f"{err[0]}\n{err[1]}")

                    view = ViewCertOutput()
                    view.set_model(strk_out)
                    view.connect("destroy", Gtk.main_quit)
                    view.show_all()
                    Gtk.main()
            else:
                self.print_info(ret, 350, 300)
        else:
            dialog.destroy()

    def enter_license(self, widget):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text="Введите лицензионный ключ:")
        dialogWindow.set_title("Лицензия КриптоПро")
        dialogWindow.set_border_width(5)
        dialogWindow.set_size_request(300, 100)
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()
        userEntry = Gtk.Entry()
        dialogBox.pack_end(userEntry, False, False, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        cpro_license = userEntry.get_text()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.OK) and (cpro_license != ''):
            l = set_license(cpro_license)
            if l[1]:
                self.print_error(f'Произошла ошибка: {l[0]}')
            else:
                self.print_simple_info('Лицензионный ключ успешно установлен')

    def enter_container_name(self, widget, old_name):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text=f"Новое имя:")
        dialogWindow.set_title("Имя контейнера")
        dialogWindow.set_border_width(5)
        dialogWindow.set_size_request(300, 100)
        dialogWindow.set_resizable(True)

        dialogBox = dialogWindow.get_content_area()
        nameEntry = Gtk.Entry()
        nameEntry.set_text(f"{old_name}_copy")
        dialogBox.pack_end(nameEntry, False, False, 0)
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
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text=f"Новое имя:")
        dialogWindow.set_title("Имя сертификата *.cer")
        dialogWindow.set_border_width(5)
        dialogWindow.set_size_request(300, 100)
        dialogWindow.set_resizable(True)

        dialogBox = dialogWindow.get_content_area()
        nameEntry = Gtk.Entry()
        nameEntry.set_text(f"{old_name}_cert")
        dialogBox.pack_end(nameEntry, False, False, 0)
        dialogWindow.show_all()
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
        dialog = Gtk.FileChooserDialog(title="Выберите файл(ы)", parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Сертификаты *.cer *.crt")
        filter.add_mime_type("Сертификаты")
        filter.add_pattern("*.cer")
        filter.add_pattern("*.CER")
        filter.add_pattern("*.crt")
        filter.add_pattern("*.CRT")
        dialog.add_filter(filter)
        dialog.set_select_multiple(True)
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
                root_view.set_model(Gtk.ListStore(str, Gdk.RGBA), True)
                root_info = install_root_cert(file, root)

                for line in root_info:
                    not_valid_before = datetime.strptime(line[5], '%d/%m/%Y  %H:%M:%S ')
                    not_valid_after = datetime.strptime(line[6], '%d/%m/%Y  %H:%M:%S ')
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                    if not_valid_after < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                    if versiontuple(get_cspversion()[2]) >= versiontuple("5.0.12000"):
                        item = 'Эмитент: %s\nСубъект: %s\nСерийный номер: %s\nSHA1 Отпечаток: %s\nНе действителен до: %s\n' \
                               'Не действителен после: %s' % (line[1], line[2], line[3], line[4], \
                                                              datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S'), \
                                                              datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S'))
                    else:
                        item = 'Эмитент: %s\nСубъект: %s\nСерийный номер: %s\nХэш SHA1: %s\nНе действителен до: %s\n' \
                               'Не действителен после: %s' % (line[1], line[2], line[3], line[4], \
                                                              datetime.strftime(not_valid_before, '%d.%m.%Y %H:%M:%S'), \
                                                              datetime.strftime(not_valid_after, '%d.%m.%Y %H:%M:%S'))
                    root_view.cert_listview.append([item, color])
                root_view.set_title("Установлен корневой сертификат")
                root_view.connect("destroy", Gtk.main_quit)
                root_view.show_all()
                Gtk.main()
        else:
            dialog.destroy()

    def delete_from_nonToken(self):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text="\nВы уверенны что хотите удалить данный сертификат?\n\n"
                                              "Эту операцию нельзя отменить.")
        dialogWindow.set_title("Подтверждение")
        dialogBox = dialogWindow.get_content_area()

        dialogWindow.show_all()
        response = dialogWindow.run()

        dialogWindow.destroy()
        return response

    def delete_from_Token(self):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL,
                                         text="\nВы уверенны что хотите удалить данный сертификат с ключевого носителя?\n\nЭту операцию нельзя отменить.")
        dialogWindow.set_title("Подтверждение")
        dialogBox = dialogWindow.get_content_area()

        dialogWindow.show_all()
        response = dialogWindow.run()

        dialogWindow.destroy()
        return response

    def open_crl(self, widget):
        dialog = Gtk.FileChooserDialog(title="Выберите файл(ы)", parent=self,
                                       action=Gtk.FileChooserAction.OPEN,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Сертификаты")
        filter.add_mime_type("Сертификаты")
        filter.add_pattern("*.crl")
        dialog.add_filter(filter)
        dialog.set_select_multiple(True)
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
            crl_view.set_model(Gtk.ListStore(str, Gdk.RGBA), True)
            for filename in file_names:
                crl_info = install_crl(filename, root)
                for line in crl_info:
                    item = ""
                    this_update = datetime.strptime(line[2], '%d/%m/%Y  %H:%M:%S ')
                    next_update = datetime.strptime(line[3], '%d/%m/%Y  %H:%M:%S ')
                    color = Gdk.RGBA(red=0, green=0, blue=0, alpha=0)
                    if next_update < datetime.utcnow():
                        color = Gdk.RGBA(red=252, green=133, blue=133, alpha=1)
                    item = ('%s\nДата выпуска: %s UTC\nДата обновления: %s UTC' %
                            (line[1], datetime.strftime(this_update, '%d.%m.%Y %H:%M:%S'),
                             datetime.strftime(next_update, '%d.%m.%Y %H:%M:%S')))
                    crl_view.cert_listview.append([item, color])
            crl_view.set_title("Установлен список отозванных сертификатов")
            crl_view.connect("destroy", Gtk.main_quit)
            crl_view.show_all()
            Gtk.main()
        else:
            dialog.destroy()

    def ask_about_root(self, widget):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.NONE,
                                         text="\nУстановить сертифиакт(ы) для локального пользователя\nили для всех сразу? (хранилище mRoot)")
        dialogWindow.set_title("Вопрос")
        dialogWindow.add_buttons("Локально", Gtk.ResponseType.CANCEL, "Для всех", Gtk.ResponseType.OK)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def ask_about_mmy(self, widget):
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.NONE,
                                         text="\nУстановить сертифиакт(ы) для локального пользователя(хранилище uMy)\nили для всех сразу(хранилище mMy)?")
        dialogWindow.set_title("Вопрос")
        dialogWindow.add_buttons("Локально", Gtk.ResponseType.CANCEL, "Для всех", Gtk.ResponseType.OK)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        return response

    def install_HDIMAGE(self, widget):
        find_hdimage = os.popen(f"/opt/cprocsp/sbin/{arch}/cpconfig -hardware reader -view | grep HDIMAGE").readlines()
        if not find_hdimage[0]:
            dialogWindow = Gtk.MessageDialog(parent=self,
                                             modal=True, destroy_with_parent=True,
                                             message_type=Gtk.MessageType.QUESTION,
                                             buttons=Gtk.ButtonsType.OK_CANCEL,
                                             text="Введите пароль root пользователя")
            dialogWindow.set_title("Создание HDIMAGE хранилища")
            dialogBox = dialogWindow.get_content_area()
            pinEntry = Gtk.Entry()
            pinEntry.set_visibility(False)
            dialogBox.pack_end(pinEntry, False, False, 0)
            dialogWindow.show_all()
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
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogWindow.set_title("Выберите контейнер")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore_all_containers)
        max_len = 0
        for elem in self.liststore_all_containers:
            if max_len < len(elem[0]):
                max_len = len(elem[0])
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Контейнеры", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_all_toggled)

        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        if max_len < 40:
            dialogWindow.set_size_request(380, 200)
            scrolled_tree.set_size_request(380, 200)
        else:
            dialogWindow.set_size_request(580, 200)
            scrolled_tree.set_size_request(580, 200)
        dialogBox.pack_end(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
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
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogWindow.set_title("Выберите контейнер с токена")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore_containers)
        max_len = 0
        for elem in self.liststore_containers:
            if max_len < len(elem[0]):
                max_len = len(elem[0])
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Контейнеры", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)

        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        if max_len < 40:
            dialogWindow.set_size_request(380, 200)
            scrolled_tree.set_size_request(380, 200)
        else:
            dialogWindow.set_size_request(580, 200)
            scrolled_tree.set_size_request(580, 200)
        dialogBox.pack_end(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def choose_dest_stores(self, liststore):
        self.liststore_dest_stores = liststore
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogWindow.set_title("Выберите 1 хранилище для экспортирования контейнера")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore_dest_stores)
        max_len = 0
        for elem in self.liststore_dest_stores:
            if max_len < len(elem[0]):
                max_len = len(elem[0])
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Хранилища", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_dest_toggled)

        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        if max_len < 40:
            dialogWindow.set_size_request(380, 200)
            scrolled_tree.set_size_request(380, 200)
        else:
            dialogWindow.set_size_request(580, 200)
            scrolled_tree.set_size_request(580, 200)
        dialogBox.pack_end(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def choose_open_cert_to_close_container(self, container):
        dialog = Gtk.FileChooserDialog(title="Выберите сертификат пользователя", parent=self,
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
                            self.print_simple_info(
                                u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                                strk_out.append("Успешно установлены корневые сертификаты:")
                                for succ in success_ca:
                                    strk_out.append(f"{succ}")

                            if len(success_cdp) > 0:
                                strk_out.append("Успешно установлены сертификаты отзыва:")
                                for succ in success_cdp:
                                    strk_out.append(f"{succ}")

                            if len(errors_ca) > 0:
                                strk_out.append("Ошибка при установке корневых сертификатов:")
                                for err in errors_ca:
                                    strk_out.append(f"{err[0]}\n{err[1]}")

                            if len(errors_cdp) > 0:
                                if len(success_ca) > 0 or len(success_cdp) > 0 or len(errors_ca) > 0:
                                    strk_out += "\n"
                                strk_out.append("Ошибка при установке сертификатов отзыва:")
                                for err in errors_cdp:
                                    strk_out.append(f"{err[0]}\n{err[1]}")

                            view = ViewCertOutput()
                            view.set_model(strk_out)
                            view.connect("destroy", Gtk.main_quit)
                            view.show_all()
                            Gtk.main()
                        else:
                            self.print_simple_info(u"Сертификат успешно установлен.")
                        return [True]
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return [False, "Отменено пользователем"]

    def install_local_cert_to_container(self, widget):
        dialog = Gtk.FileChooserDialog(title="Выберите сертификат пользователя", parent=self,
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
                                self.print_error("Необходимо выбрать 1 контейнер\n"
                                                         "для настройки связывания")
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
                                        self.print_simple_info(
                                            u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                                            strk_out.append("Успешно установлены корневые сертификаты:")
                                            for succ in success_ca:
                                                strk_out.append(f"{succ}")

                                        if len(success_cdp) > 0:
                                            strk_out.append("Успешно установлены сертификаты отзыва:")
                                            for succ in success_cdp:
                                                strk_out.append(f"{succ}")

                                        if len(errors_ca) > 0:
                                            strk_out.append("Ошибка при установке корневых сертификатов:")
                                            for err in errors_ca:
                                                strk_out.append(f"{err[0]}\n{err[1]}")

                                        if len(errors_cdp) > 0:
                                            strk_out.append("Ошибка при установке сертификатов отзыва:")
                                            for err in errors_cdp:
                                                strk_out.append(f"{err[0]}\n{err[1]}")

                                        view = ViewCertOutput()
                                        view.set_model(strk_out)
                                        view.connect("destroy", Gtk.main_quit)
                                        view.show_all()
                                        Gtk.main()
                                    else:
                                        self.print_simple_info(
                                            "Сертификат успешно связан с контейнером.")
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
                        self.print_simple_info(
                            "Контейнер успешно скопирован\n"
                            "и связан с сертификатом.\n"
                            "Сейчас будут установлены дополнительные сертификаты.")
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
                            strk_out.append("Успешно установлены корневые сертификаты:")
                            for succ in success_ca:
                                strk_out.append(f"{succ}")

                        if len(success_cdp) > 0:
                            strk_out.append("Успешно установлены сертификаты отзыва:")
                            for succ in success_cdp:
                                strk_out.append(f"{succ}")

                        if len(errors_ca) > 0:
                            strk_out.append("Ошибка при установке корневых сертификатов:")
                            for err in errors_ca:
                                strk_out += f"{err[0]}\n{err[1]}\n"

                        if len(errors_cdp) > 0:
                            strk_out.append("Ошибка при установке сертификатов отзыва:")
                            for err in errors_cdp:
                                strk_out.append(f"{err[0]}\n{err[1]}")

                        view = ViewCertOutput()
                        view.set_model(strk_out)
                        view.connect("destroy", Gtk.main_quit)
                        view.show_all()
                        Gtk.main()
                    else:
                        self.info_class.print_simple_info(
                            "Контейнер успешно скопирован\n"
                            "и связан с сертификатом.")
                    return True
        # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
        if not self.output_code_token:
            dialog = Gtk.FileChooserDialog(title="Выберите сертификат пользователя", parent=self,
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
                                self.print_simple_info(
                                    u"Сертификат успешно установлен.\nСейчас будут установлены дополнительные сертификаты.")
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
                                    strk_out += "Успешно установлены корневые сертификаты:\n"
                                    for succ in success_ca:
                                        strk_out.append(f"{succ}")

                                if len(success_cdp) > 0:
                                    if len(success_ca) > 0:
                                        strk_out += "\n"
                                    strk_out.append("Успешно установлены сертификаты отзыва:")
                                    for succ in success_cdp:
                                        strk_out.append(f"{succ}")

                                if len(errors_ca) > 0:
                                    strk_out.append("Ошибка при установке корневых сертификатов:")
                                    for err in errors_ca:
                                        strk_out += f"{err[0]}\n{err[1]}\n"

                                if len(errors_cdp) > 0:
                                    if len(success_ca) > 0 or len(success_cdp) > 0 or len(errors_ca) > 0:
                                        strk_out += "\n"
                                    strk_out.append("Ошибка при установке сертификатов отзыва:")
                                    for err in errors_cdp:
                                        strk_out.append(f"{err[0]}\n{err[1]}")

                                view = ViewCertOutput()
                                view.set_model(strk_out)
                                view.connect("destroy", Gtk.main_quit)
                                view.show_all()
                                Gtk.main()
                            else:
                                self.info_class.print_simple_info(
                                    "Контейнер успешно скопирован\n"
                                    "и связан с сертификатом.")
                            self.output_code_token = True
                            return True
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.output_code_token = False
                return False

    def install_new_cert_to_container(self, container):
        dialog = Gtk.FileChooserDialog(title="Выберите сертификат пользователя", parent=self,
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

    def return_output_code_token(self):
        return self.output_code_token

    def choose_folder_dialog(self, widget):
        dialog = Gtk.FileChooserDialog(title="Выберите директорию", parent=self,
                                       action=Gtk.FileChooserAction.SELECT_FOLDER,
                                       )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           "Выбрать директорию", Gtk.ResponseType.OK)
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
        # сделать окно выбора контейнера из списка распознанных системой
        # команда из ТГ по экспортированияю контейнера попробовать выполнить автоинсталл,
        # в случае неудачи сделать по БЗ с явным указание открытого ключа
        self.liststore_flashes = liststore
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogWindow.set_title("Выберите контейнер с usb-flash накопителя")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore_flashes)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Контейнеры", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled_flash)
        max_len = 0
        for elem in self.liststore_flashes:
            if max_len < len(elem[0]):
                max_len = len(elem[0])
        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)

        if max_len < 40:
            dialogWindow.set_size_request(380, 200)
            scrolled_tree.set_size_request(380, 200)
        else:
            dialogWindow.set_size_request(580, 200)
            scrolled_tree.set_size_request(580, 200)
        dialogBox.pack_end(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def call_secretnet_configs(self, for_what, udev):
        file = f"/etc/udev/rules.d/87-{udev}_usb.rules"
        if not os.path.exists(file):
            dialogWindow = Gtk.MessageDialog(parent=self,
                                             modal=True, destroy_with_parent=True,
                                             message_type=Gtk.MessageType.QUESTION,
                                             buttons=Gtk.ButtonsType.OK_CANCEL,
                                             text="Введите пароль root пользователя, после применения\nпотребуется переподключить usb-flash накопитель")
            dialogWindow.set_title(f"Настройка udev правила для {for_what}")
            dialogBox = dialogWindow.get_content_area()
            pinEntry = Gtk.Entry()
            pinEntry.set_visibility(False)
            dialogBox.pack_end(pinEntry, False, False, 0)
            dialogWindow.show_all()
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
        # сделать окно выбора контейнера из списка распознанных системой
        # команда из ТГ по экспортированияю контейнера попробовать выполнить автоинсталл,
        # в случае неудачи сделать по БЗ с явным указание открытого ключа
        self.liststore_hdimage_containers = liststore
        dialogWindow = Gtk.MessageDialog(parent=self,
                                         modal=True, destroy_with_parent=True,
                                         message_type=Gtk.MessageType.QUESTION,
                                         buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogWindow.set_title("Выберите контейнер из hdimage")
        dialogWindow.set_resizable(True)
        dialogBox = dialogWindow.get_content_area()

        treeview = Gtk.TreeView(model=self.liststore_hdimage_containers)
        max_len = 0
        for elem in self.liststore_hdimage_containers:
            if max_len < len(elem[0]):
                max_len = len(elem[0])
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Контейнеры", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_hdimage_toggled)

        column_toggle = Gtk.TreeViewColumn("Выбранный", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        sel = treeview.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.add(treeview)
        if max_len < 40:
            dialogWindow.set_size_request(380, 200)
            scrolled_tree.set_size_request(380, 200)
        else:
            dialogWindow.set_size_request(580, 200)
            scrolled_tree.set_size_request(580, 200)
        dialogBox.pack_end(scrolled_tree, True, True, 0)
        dialogWindow.show_all()
        response = dialogWindow.run()
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.CANCEL):
            return False
        else:
            return True

    def install_cert_from_or_to_usb_flash(self, container):
        # Требуется попробовать получить открытую часть хранилища автоматически, установленного локально в HDIMAGE
        self.output_code_flash = False
        csptest = subprocess.Popen(['/opt/cprocsp/bin/%s/csptest' % arch, '-keyset', '-enum_cont', '-unique', '-fqcn',
                                    '-verifyc'], stdout=subprocess.PIPE)
        output = csptest.communicate()[0].decode('cp1251').encode('utf-8').decode("utf-8")
        certs = []
        for line in output.split("\n"):
            if "HDIMAGE" in line and container in line:
                certs.append(line)
        for cert in certs:
            cert = cert.split("|")[1].strip()
            output = os.popen(f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -cont '{cert}'").readlines()
            for l in output:
                if "[ErrorCode: 0x00000000]\n" in l:
                    self.output_code_flash = True
                    return True
        # Вариант с открытой частью не удался, предлагаем пользователю самому выбрать сертификат для закрытой части.
        if not self.output_code_flash:
            dialog = Gtk.FileChooserDialog(title="Выберите сертификат пользователя", parent=self,
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
            domain_name = os.popen("echo $USERNAME").readlines()[0]
            if "\\" in domain_name:
                domain_name = domain_name.split("\\")[1]
            elif "@" in domain_name:
                domain_name = domain_name.split("@")[0]
            find_name = os.popen(f"find /home/ -maxdepth 2 -name *{domain_name}*").readlines()[0].strip()
            dialog.set_current_folder(f"'{find_name}'")
            dialog.set_select_multiple(False)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_name = dialog.get_filename()
                dialog.destroy()
                cert = certs[0].split("|")[1].strip()
                if file_name:
                    output = os.popen(
                        f"/opt/cprocsp/bin/{arch}/certmgr -inst -store uMy -file '{file_name}' -cont '{cert}'").readlines()
                    for l in output:
                        if "[ErrorCode: 0x00000000]\n" in l:
                            self.output_code_flash = True
                            return True
            elif response == Gtk.ResponseType.CANCEL:
                self.output_code_flash = False
                return False

    def return_output_code_flash(self):
        return self.output_code_flash

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
    window = Gtk.ApplicationWindow()
    window.set_title(re.sub("\n", "", module_name()))
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_default_icon_name('token-manager')
    containerr = Gtk.Notebook()
    containerr.set_show_tabs(False)
    paned = Gtk.Paned()
    paned.add2(containerr)
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    main_box.pack_start(paned, True, True, 0)
    combox = TokenUI(main_box, True)
    containerr.append_page(combox)
    window.add(main_box)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


def module_name():
    return f"Ключевые носители и сертификаты ({arch})"


def module_icon():
    return "token-manager.resized.png"

if __name__ == "__main__":
    window = main()

