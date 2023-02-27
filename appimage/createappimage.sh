#!/bin/bash
rm -rf ./Token_Manager-x86_64.AppImage
rm -rf ./AppDir
mkdir -p ./AppDir
cd
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

chmod +x ./AppDir/token-manager.desktop
chmod +x ./AppDir/AppRun
chmod +x ./appimagetool
ARCH=x86-64 ./appimagetool ./AppDir
chmod +x ./Token_Manager-x86_64.AppImage
./Token_Manager-x86_64.AppImage
