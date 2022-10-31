#
# spec file for package token-manager
#

Name:        token-manager
Version:     2.3
Release:     1%{dist}.2

BuildArch:   noarch

Summary:     Certificate manager for CryptoPro CSP
Summary(ru): Менеджер сертификатов для CryptoPro CSP
License:     MIT
Group:       System Environment/Base
Url:         https://github.com/wolandius/token-manager

Source0:     %{name}-%{version}.tar.gz

Requires:    usermode
Requires:    opensc
Requires:    xdg-utils
Requires:    polkit
Requires:    realmd

%description
A GTK front-end for Crypto Pro CSP for RED OS and GosLinux.

%description -l ru
Графическая оболочка GTK для Crypto Pro CSP для операционных систем РЕД ОС и ГосЛинукс.

%package ia32
Summary:     Certificate manager for 32-bit CryptoPro CSP
Summary(ru): Менеджер сертификатов для 32-битной CryptoPro CSP
BuildArch:   noarch
Requires:    %{name}

%description -l ru ia32
Графическая оболочка GTK для 32-битной Crypto Pro CSP для операционных систем РЕД ОС и ГосЛинукс.

%prep
%setup -q

%install
mkdir -p %{buildroot}/%{_bindir}
ln -sf /usr/bin/consolehelper %{buildroot}%{_bindir}/cpconfig-amd64
ln -sf /usr/bin/consolehelper %{buildroot}%{_bindir}/cpconfig-ia32
%{__install} -m 0755 %{name}.py %{buildroot}%{_bindir}/%{name}.py

mkdir -p %{buildroot}/%{_datadir}/pixmaps
mkdir -p %{buildroot}/%{_datadir}/applications
%{__install} -m 0644 %{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__install} -m 0755 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
%{__install} -m 0755 %{name}-ia32.desktop %{buildroot}%{_datadir}/applications/%{name}-ia32.desktop

mkdir -p %{buildroot}/%{_sysconfdir}/pam.d
mkdir -p %{buildroot}/%{_sysconfdir}/security/console.apps
%{__install} -m 0644 cpconfig-pam %{buildroot}%{_sysconfdir}/pam.d/cpconfig-amd64
%{__install} -m 0644 cpconfig-pam %{buildroot}%{_sysconfdir}/pam.d/cpconfig-ia32
%{__install} -m 0644 cpconfig-amd64 %{buildroot}%{_sysconfdir}/security/console.apps/cpconfig-amd64
%{__install} -m 0644 cpconfig-ia32 %{buildroot}%{_sysconfdir}/security/console.apps/cpconfig-ia32
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
%{__install} -m 0644 LICENSE.md %{buildroot}%{_datadir}/doc/%{name}/LICENSE.md
%{__install} -m 0644 README.md %{buildroot}%{_datadir}/doc/%{name}/README.md
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
%{__install} -m 0644 org.freedesktop.policykit.pkexec.policy %{buildroot}%{_datadir}/polkit-1/actions/org.freedesktop.policykit.pkexec.policy

%{__install} -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
%{__install} -m 0755 %{name}-ia32 %{buildroot}%{_bindir}/%{name}-ia32


%post
xdg-desktop-menu install --mode system %{_datadir}/applications/%{name}.desktop

%post ia32
xdg-desktop-menu install --mode system %{_datadir}/applications/%{name}-ia32.desktop

%files
%{_datadir}/doc/%{name}/LICENSE.md
%{_datadir}/doc/%{name}/README.md
%{_bindir}/cpconfig-amd64
%attr(0755,root,root) %{_bindir}/%{name}.py
%attr(0755,root,root) %{_bindir}/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.pkexec.policy
%{_sysconfdir}/pam.d/cpconfig-amd64
%{_sysconfdir}/security/console.apps/cpconfig-amd64
%{_datadir}/pixmaps/token-manager.png
%attr(0755,root,root) %{_datadir}/applications/%{name}.desktop

%files ia32
%{_bindir}/cpconfig-ia32
%attr(0755,root,root) %{_bindir}/%{name}-ia32
%{_sysconfdir}/pam.d/cpconfig-ia32
%{_sysconfdir}/security/console.apps/cpconfig-ia32
%attr(0755,root,root) %{_datadir}/applications/%{name}-ia32.desktop

%changelog
* Mon Oct 17 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:2.3-1
- added error window for unsupported encodings on token

* Thu Sep 01 2022 Vladlen Murylyov <vladlen.murylyov@red-soft.ru> - 0:2.2-1
- Replace beesu to pkexec in cases if root is blocked in OS

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
