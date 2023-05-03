#!/bin/bash
if [ ! -f "./appimagetool" ]; then
    wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O ./appimagetool
fi
rm -rf ./token-manager-ro$1.AppImage
rm -rf ./AppDir
mkdir -p ./AppDir
cd ..
python3 ./setup.py install --root=./appimage/AppDir --prefix=usr
cd appimage

cp AppRun ./AppDir/
cp ../data/token-manager.desktop ./AppDir/
cp ../data/token-manager.png ./AppDir/
pushd ./redos_rpms
cp -r ./usr ../AppDir/
cp -r ./etc ../AppDir/
cp -r ./var ../AppDir/
popd

pushd ./AppDir/usr/bin
ln -sf ./consolehelper ./cpconfig-amd64
ln -sf ./consolehelper ./cpconfig-ia32
popd

if [ $1 = "72" ]; then
   sed -i 's|version="3.24"|version="3.22"|g'  ./AppDir/usr/share/token_manager/ui/token_manager.glade;
   sed -i 's|version="3.24"|version="3.22"|g'  ./AppDir/usr/share/token_manager/ui/templates.glade;
fi

chmod +x ./AppDir/token-manager.desktop
chmod +x ./AppDir/AppRun
chmod +x ./appimagetool
ARCH=x86-64 ./appimagetool ./AppDir
chmod +x ./Token_Manager-x86_64.AppImage
mv Token_Manager-x86_64.AppImage token-manager-ro$1.AppImage
./token-manager-ro$1.AppImage
