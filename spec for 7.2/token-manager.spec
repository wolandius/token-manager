#
# spec file for package token-manager
#

Name:           token-manager
Version:        5.2.1
Release:        1%{dist}.2

BuildArch:      noarch

Summary:        Certificate manager for CryptoPro CSP
Summary(ru):    Менеджер сертификатов для CryptoPro CSP
License:        MIT
Group:          System Environment/Base
Url:            https://github.com/wolandius/token-manager

Source0:        %{name}-%{version}.tar.gz

Buildrequires:  python3
Buildrequires:  python3-devel
Buildrequires:  python3-setuptools

Requires:       opensc
Requires:       python3-chardet
Requires:       usermode
Requires:       xdg-utils
Requires:       realmd
Requires:       procps-ng
Requires:       wget
Requires:       polkit

%description
A GTK front-end for Crypto Pro CSP for RED OS and GosLinux.

%description -l ru
Графическая оболочка GTK для Crypto Pro CSP для операционных систем РЕД ОС и ГосЛинукс.

%package ia32
Summary:        Certificate manager for 32-bit CryptoPro CSP
Summary(ru):    Менеджер сертификатов для 32-битной CryptoPro CSP
BuildArch:      noarch
Requires:       %{name}

%description -l ru ia32
Графическая оболочка GTK для 32-битной Crypto Pro CSP для операционных систем РЕД ОС и ГосЛинукс.

%prep
%setup -q
rm -rf %{name}.egg-info

%build
python3 setup.py build

%install
mkdir -p %{buildroot}/%{_bindir}

ln -sf /usr/bin/consolehelper %{buildroot}%{_bindir}/cpconfig-amd64
ln -sf /usr/bin/consolehelper %{buildroot}%{_bindir}/cpconfig-ia32

python3 setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%post
xdg-desktop-menu install --mode system %{_datadir}/applications/%{name}.desktop
sed -i 's|version="3.24"|version="3.22"|g'  %{_datadir}/token_manager/ui/token_manager.glade
sed -i 's|version="3.24"|version="3.22"|g'  %{_datadir}/token_manager/ui/templates.glade

%posttrans
VERSION=%{version}
for f in /usr/lib/python3*/site-packages/token_manager*egg*;
do
  if [ -d "$f" ] && [ "$f" != "/usr/lib/python3"*"/site-packages/token_manager-$VERSION"* ]; then
    rm -rf $f ;
  fi;
done


%post ia32
xdg-desktop-menu install --mode system %{_datadir}/applications/%{name}-ia32.desktop

%files -f INSTALLED_FILES
%license LICENSE.md
%doc README.md Changelog
%{_bindir}/cpconfig-amd64
%exclude %{_datadir}/applications/%{name}-ia32.desktop
%exclude  /usr/lib/python3*/site-packages/token_manager/*/*.pyc
%exclude  %{_sysconfdir}/pam.d/cpconfig-ia32

%files ia32
%{_bindir}/cpconfig-ia32
%{_sysconfdir}/pam.d/cpconfig-ia32
%{_datadir}/applications/%{name}-ia32.desktop

%changelog
* Wed May 03 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:5.2.1-1
- fix gtk24 version in GLADE for RED OS7.2

* Thu Apr 20 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:5.2-1
- replace regex parse in certs view with new dictionary funcs
- added full support for languages in appimage mode


* Fri Apr 07 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:5.1-1
- improved certs parse logic in select_token function

* Fri Mar 31 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:5.0-1
- added UI files
- added translate files
- added ask_about_extras dialog
- fix rules error with extra certs wget

* Thu Feb 02 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:4.2-1
- added compitibility with appimage format
- fix in set_license function

* Tue Jan 17 2023 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:4.1-1
- hide ask_about_mmy dialog on crypto 4
- improve ViewCertOutput and InfoClass dialogs

* Thu Nov 24 2022 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0:4.0-2
- solve conflict between desktop-files

* Wed Nov 23 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:4.0-1
- changed project structure to use setup.py on build
- rebased context menu
- added functions for mMy install certs
- added function for manual linking cert and cont

* Wed Nov 09 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:3.0-1
- added chain view in certificate window
- added auto chain install for uMy, token and hdimage certificates

* Thu Sep 01 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:2.2-1
- Replace beesu with pkexec in cases where root is blocked in OS

* Thu Apr 14 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:2.1-1
- Removed key -dn and replaced with -keyid
- Added ru description to spec
- Added new function export_container_cert
- regex impovements, for userfriendly reading
- rebased src to use archive as SOURCE0

* Mon Feb 21 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:2.0-1
- Fixed non-fatal error in refresh
- Hide button "connect as reader", because this one not used
- added aliases for name token-manager.py - token-manager and token-manager-ia32
- added shortcut for ia32
- devide binary packages for main and ia32
- rebased regex logic in get_store_certs to show more home certs with redwine use

* Wed Feb 09 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.9-1
- changed logic for certmgr -inst -inst_to_cont
  -file -cont, now numeric container name uses
- added mask *.CER and *.CRT in addition to *.cer, *.cer
- improved usb-flash containers export logic,
  now available to rename it

* Mon Jan 24 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.8-1
- fixed update list in case of delete containers

* Fri Jan 14 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.7-1
- added change names instead of name_copy for containers export
- added destination choose for containers export
- fix in token serial numbers
- improvements in write_cert output

* Thu Dec 30 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.6-1
- added function for install cert to container

* Thu Dec 23 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.5-1
- fix in serial = int(output[:11].decode('utf-8').replace(' ', ''), 16)
- added hand choose arch for debugmode

* Thu Dec 02 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.4-1
- bug fixe in def delete_from_Token(self)
- fixed warning  Warning: unable to set property
  'background' of type 'gchararray' from value of type 'GdkRGBA'

* Thu Nov 25 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.3-2
- bug fixes in self.name and if tokens not exists
- added version key for terminal

* Mon Nov 22 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.3-1
- added option '--debug-output' for analyzing main funcs worikng

* Sun Sep 26 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:1.1-1
- added check of pcscd status and enable it to autorun
- fixed work for domain users without SecretNet

* Mon Jul 26 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.4-4
- cosmetic update, that makes available to use system colors
  in most gtk app items instead of hardcoded #ffffff

* Thu Jul 15 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.4-3
- improved compatibility for cryptocpro4 non-cert rc5 version 4.0.9975

* Wed Jul 7 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.4-2
- improved compatibility for cryptocpro cert rc2 version 12000

* Fri Jul 2 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.4-1
- improved compatibility for cryptocpro cert rc2

* Tue Jun 29 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.4-0
- improved logic for secretnet users
- added new submenu for usefull links

* Fri Jun 18 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.3-3
- changed delete window size from 1200*500 to 1000*500
- fixed delete certs from mRoot
- changed text in dialog buttons for mRoot store certs install
- some fixes in u/mRoot certs install

* Sat Jun 5 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.3-2
- fixed error in check supported cryptopro version

* Thu Jun 3 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.3-1
- added new window for choose mRoot or uRoot store
- added check for non supported cryptopro version
- fix changed crypto5 version to cert version
- small cosmetic fix in notification windows

* Mon May 31 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.2-1
- cosmetic update for notification windows
- added missing gui for start check cryptopro
- changed pin-code change logic
- added keys for hand-choose of arch cryptopro. actual in cases of both archs on pc

* Wed May 26 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13.1-1
- Made fixes for correct work with domain users' names (such as DOMAIN\USERNAME or USERNAME@DOMAIN)
- Improved logic in choosing of flash/token

* Mon May 17 2021 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.13-1
- Added copy containers from tokens or usb-flash to HDIMAGE and choose certificate for containers
- Added work for secretnet with specific domains

* Tue Feb 09 2021 Alexandr Subbotin <alexander.subbotin@red-soft.ru> - 0.12-9
- Fix bugs

* Tue Dec 22 2020 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0.12-8
- Rebuild for work on python3, GTK3, cryptopro 4 and 5

* Tue Dec 22 2020 Alexandr Subbotin <alexander.subbotin@red-soft.ru> - 0.12-7
- Rebuild for os73 and add backward compatibility

* Mon Mar 25 2019 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0.12-6
- apply commit 5b05054 from git

* Mon Mar 12 2018 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0.12-5
- apply commit 51687e240e8ce9d03c821644273fb7671fd25ecd from git

* Thu Feb 15 2018 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0.12-4
- apply commit 51687e240e8ce9d03c821644273fb7671fd25ecd from git

* Wed Jul 26 2017 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0.12-2
- rebuild for RedOS

* Fri Jul 14 2017 Alexey Rodionov <alexey.rodionov@red-soft.ru> - 0.12-1
- rebuild for GosLinux 6
- add LICENSE and README files to rpm

* Fri Apr 07 2017 Boris Makarenko <bmakarenko90@gmail.com> - 0.12
- Release 0.12
- Compatibility with CryptoPro CSP 4.0

* Sun Oct 30 2016 Boris Makarenko <bmakarenko90@gmail.com> - 0.11
- Release 0.11
- Installing certificates to uMy store from file

* Wed Jul 06 2016 Boris Makarenko <bmakarenko90@gmail.com> - 0.10
- Release 0.10-1
- Filter list of root certificates and CRLs

* Wed May 04 2016 Boris Makarenko <bmakarenko90@gmail.com> - 0.10
- Release 0.10
- Displaying the token's serial number

* Tue Feb 09 2016 Boris Makarenko <bmakarenko90@gmail.com> - 0.9
- Release 0.9
- Personal and root certificate storages
- Displaying complete and translated into Russian info about certificates

* Wed Feb 03 2016 Boris Makarenko <bmakarenko90@gmail.com> - 0.8
- Release 0.8
- Hardware reader setup
- Remastered viewer windows

* Thu Aug 06 2015 Boris Makarenko <bmakarenko90@gmail.com> - 0.7
- Release 0.7
- Added cache PIN feature

* Wed Mar 18 2015 Boris Makarenko <bmakarenko90@gmail.com> - 0.6
- Release 0.6
- Display CSP version
- Obsolete CSP version warning

* Wed Dec 24 2014 Boris Makarenko <bmakarenko90@gmail.com> - 0.5
- Release 0.5
- Added delete container feature

* Tue Dec 23 2014 Boris Makarenko <bmakarenko90@gmail.com> - 0.4
- Release 0.4
- Added change PIN feature

* Fri Dec 19 2014 Boris Makarenko <bmakarenko90@gmail.com> - 0.3
- Release 0.3
- View installed root certificates and CRLs

* Mon Dec 08 2014 Boris Makarenko <bmakarenko90@gmail.com> - 0.2
- Release 0.2
- Added features: Set license, View license, Install root certificate, Install CRL

* Thu Dec 04 2014 Boris Makarenko <bmakarenko90@gmail.com> - 0.1
- Initial build
