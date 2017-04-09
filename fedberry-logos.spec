Name:       fedberry-logos
Version:    25.1
Release:    1%{?dist}
Summary:    Icons and pictures
Group:      System Environment/Base
URL:        https://github.com/fedberry/fedberry-logos
Source0:    https://github.com/fedberry/fedberry-logos/raw/master/%{name}-%{version}.tar.xz
#The KDE Logo is under a LGPL license (no version statement)
License:    GPLv2 and LGPLv2+
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Obsoletes:  fedora-logos
Provides:   fedora-logos
Conflicts:  fedora-logos
Provides:   system-logos
BuildRequires: hardlink
# For _kde4_* macros:
BuildRequires: kde-filesystem
# For generating the EFI icon
BuildRequires: libicns-utils
# For optimizing png files
BuildRequires: optipng
# For generating the EFI icon
BuildRequires: ImageMagick
Requires(post): coreutils

%description
The fedberry-logos package contains various image files which can be
used by the bootloader, anaconda, and other related tools.

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/firstboot/themes/generic
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/generic
done

mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.vol %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora-media.vol  %{buildroot}%{_datadir}/pixmaps/bootloader

mkdir -p %{buildroot}%{_datadir}/pixmaps/splash
for i in gnome-splash/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps/splash
done

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
for i in plymouth/charge/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
done

for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  pushd $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  ln -s ../../../hicolor/$size/apps/fedberry-logo-icon.png icon-panel-menu.png
  ln -s ../../../hicolor/$size/apps/fedberry-logo-icon.png gnome-main-menu.png
  ln -s ../../../hicolor/$size/apps/fedberry-logo-icon.png kmenu.png
  ln -s ../../../hicolor/$size/apps/fedberry-logo-icon.png start-here.png
  popd
  for i in icons/hicolor/$size/apps/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  done
done

mkdir -p $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/48x48/apps/
install -p -m 644 icons/hicolor/48x48/apps/anaconda.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/48x48/apps/
mkdir -p $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/
install -p -m 644 icons/hicolor/scalable/apps/anaconda.svg $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_datadir}/icons/hicolor/16x16/apps/fedberry-logo-icon.png favicon.png
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/fedberry-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg
install -p -m 644 icons/hicolor/scalable/apps/anaconda.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/anaconda.svg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
ln -s ../apps/start-here.svg .
popd

(cd anaconda; make DESTDIR=%{buildroot} install)

# save some dup'd icons
/usr/sbin/hardlink -v %{buildroot}/usr

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/Bluecurve || :
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor || :
  touch --no-create %{_datadir}/icons/Bluecurve || :
  touch --no-create %{_datadir}/icons/Fedora || :
  touch --no-create %{_kde4_iconsdir}/oxygen ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Fedora &>/dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Fedora &>/dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING-kde-logo README
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/boot/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/icons/Bluecurve/*/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/plymouth/themes/charge/*
%{_kde4_iconsdir}/oxygen/


%changelog
* Thu Apr 06 2017 Vaughan <devel @ agrez dot net> - 25.1-1
- Update FedBerry logos and icons for f25 release
- Add FedBerry icons for plymouth 'Charge' theme

* Mon Jan 23 2017 Vaughan <devel @ agrez dot net> - 25.0-1
- Drop powered-by logo
- Remove x86 arch specific code
- Source0 now compressed using xz

* Tue Sep 06 2016 Vaughan <devel @ agrez dot net> - 24.0-1
- Rename package
- Add FedBerry logos and icons
- Update spec & bump release

* Thu Jun 16 2016 Vaughan <vaughan at agrez dot net> - 17.0.1-2
- Rebuild for FedBerry 24

* Sun Nov 08 2015 Vaughan <vaughan at agrez dot net> - 17.0.1-1
- Fix missing initial-setup gui buttons:
  added topbar-bg.png & sidebar-bg.png to /usr/share/anaconda/pixmaps/

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  2 2012 Bill Nottingham <notting@redhat.com> - 17.0.0-1
- update for Fedora 17 - .vol files for mactel boot

* Fri Oct 14 2011 Bill Nottingham <notting@redhat.com> - 16.0.0-1
- update syslinux & firstboot splashes for F16

* Tue Mar 22 2011 Bill Nottingham <notting@redhat.com> - 15.0.0-1
- update for Fedora 15

* Fri Dec 17 2010 Matthew Garrett <mjg@redhat.com> - 14.0.2-1
- add an icon for Mac EFI bootloaders

* Mon Nov 29 2010 Bill Nottingham <notting@redhat.com> - 14.0.1-3
- prereq coreutils (#657766)

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 14.0.1-2
- s/Fedora-KDE/oxygen/ icons (#615621)
- use hardlink to save a little space
 
* Tue Sep 14 2010 Bill Nottingham <notting@redhat.com> - 14.0.1-1
- fix for new anaconda paths

* Mon Sep 13 2010 Bill Nottingham <notting@redhat.com> - 14.0-1
- update for Fedora 14

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 13.0.2-1
- sync with current anaconda reality (#618598, <jkeating@redhat.com>)

* Sat Jul 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 13.0.1-3
- fix %%postun scriptlet error

* Fri Jun 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 13.0.1-2
- Fedora-KDE icons are now fedora-kde-icons-theme, not kde-settings
- include icon scriplets
- drop ancient Conflicts: kdebase ...

* Tue May  4 2010 Bill Nottingham <notting@redhat.com> - 13.0.1-1
- Add logos to make firstboot work

* Mon May  3 2010 Bill Nottingham <notting@redhat.com> - 13.0-1
- Update for Fedora 13

* Sat Dec 26 2009 Fabian Affolter <fabian@bernewireless.net> - 12.2-3
- Changed SourceO to upstream link
- Added URL and README
- Added version to LGPL of the KDE logo
- Minor cosmetic layout changes

* Wed Nov  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12.2-2
- kde icon installation

* Fri Oct 30 2009 Bill Nottingham <notting@redhat.com> - 12.2-1
- tweak anaconda.png/svg to match rest of icons (<duffy@redhat.com>)

* Fri Oct 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12.1-1
- 12.1 (add generic versions of anaconda.png/svg)

* Thu Oct  1 2009 Bill Nottingham <notting@redhat.com> - 12.0-1
- update for F12 (<duffy@redhat.com>)

* Tue May 12 2009 Bill Nottingham <notting@redhat.com> - 11.0.1-1
- Add new plymouth artwork (#500239)

* Wed Apr 22 2009 Bill Nottingham <notting@redhat.com> - 11.0.0-1
- updates for Fedora 11

* Wed Dec  3 2008 Bill Nottingham <notting@redhat.com> - 10.0.2-1
- fix syslinux splash (accidentally branded)

* Tue Oct 28 2008 Bill Nottingham <notting@redhat.com> - 10.0.1-1
- incorporate KDE logo into upstream source distribution
- fix system-logo-white.png for compiz bleeding (#468258)

* Mon Oct 27 2008 Jaroslav Reznik <jreznik@redhat.com> - 10.0.0-3
- Solar Comet generic splash logo redesign

* Sun Oct 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 10.0.0-2
- Add (current version of) KDE logo for SolarComet KSplash theme

* Thu Oct 23 2008 Bill Nottingham <notting@redhat.com> - 10.0.0-1
- update for current fedora-logos, with Solar theme

* Fri Jul 11 2008 Bill Nottingham <notting@redhat.com> - 9.99.0-1
- add a system logo for plymouth's spinfinity plugin

* Tue Apr 15 2008 Bill Nottingham <notting@redhat.com> - 9.0.0-1
- updates for current fedora-logos (much thanks to <duffy@redhat.com>)
- remove KDE Infinity splash
 
* Mon Oct 29 2007 Bill Nottingham <notting@redhat.com> - 8.0.2-1
- Add Infinity splash screen for KDE

* Thu Sep 13 2007 Bill Nottingham <notting@redhat.com> - 7.92.1-1
- add powered-by logo (#250676)
- updated rhgb logo (<duffy@redhat.com>)

* Tue Sep 11 2007 Bill Nottinghan <notting@redhat.com> - 7.92.0-1
- initial packaging. Forked from fedora-logos, adapted from the Fedora
  Art project's Infinity theme
