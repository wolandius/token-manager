#!/bin/bash
mkdir -p ~/rpmbuild/SPECS ~/rpmbuild/SOURCES ~/git_projects/token-manager/
cp spec\ for\ 7.2/token-manager.spec ~/rpmbuild/SPECS/
cp token-manager.py ~/rpmbuild/SOURCES/
cp token-manager.desktop ~/rpmbuild/SOURCES/
cp token-manager.png ~/rpmbuild/SOURCES/
cp cpconfig-amd64 ~/rpmbuild/SOURCES/
cp cpconfig-ia32 ~/rpmbuild/SOURCES/
cp cpconfig-pam ~/rpmbuild/SOURCES/
cp LICENSE.md ~/rpmbuild/SOURCES/
cp README.md ~/rpmbuild/SOURCES/
rpmbuild -ba ~/rpmbuild/SPECS/token-manager.spec

cp spec\ for\ 7.3/token-manager.spec ~/rpmbuild/SPECS/
rpmbuild -ba ~/rpmbuild/SPECS/token-manager.spec

# comment lines if not exist
cp -f ~/rpmbuild/RPMS/noarch/token-manager-$1.el7.2.noarch.rpm ~/git_projects/token-manager/
cp -f ~/rpmbuild/RPMS/noarch/token-manager-$1.el7.3.noarch.rpm ~/git_projects/token-manager/
cp -f ~/rpmbuild/SRPMS/token-manager-$1.el7.2.src.rpm ~/git_projects/token-manager/
cp -f ~/rpmbuild/SRPMS/token-manager-$1.el7.3.src.rpm ~/git_projects/token-manager/