#!/bin/bash

cd ~/git_projects/token-manager/data
intltool-extract --type=gettext/glade ui/token_manager.glade
intltool-extract --type=gettext/glade ui/templates.glade
cd ~/git_projects/token-manager/data/locale
xgettext --language=Python --keyword=_ --keyword=N_ --output=token_manager.pot \
~/git_projects/token-manager/src/token_manager/TokenManager.py \
~/git_projects/token-manager/data/ui/token_manager.glade.h \
~/git_projects/token-manager/data/ui/templates.glade.h




