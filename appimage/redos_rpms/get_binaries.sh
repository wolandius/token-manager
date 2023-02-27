#!/bin/bash
rm -rf ./etc
rm -rf ./usr
rm -rf ./var

dnf download opensc python3-chardet usermode xdg-utils realmd procps-ng wget polkit
rm -rf ./*.i686.rpm
for f in ./*.rpm; do
  rpm2cpio "$f" | cpio -idmv
done
rm -rf ./usr/share/doc
rm -rf ./usr/share/licenses
rm -rf ./usr/share/locale
rm -rf ./usr/share/man
rm -rf *.rpm

