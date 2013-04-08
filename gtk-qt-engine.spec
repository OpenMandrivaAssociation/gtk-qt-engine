%define libname %mklibname gtk-qt-engine
%define snapshot r5

Summary:	Allow GTK to use Qt widget styles
Name:		gtk-qt-engine
Version:	1.1
Release:	5.%{snapshot}.7
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		http://gtk-qt.ecs.soton.ac.uk/
Source0:	http://gtk-qt.ecs.soton.ac.uk/files/%{version}/%{name}-%{version}-%{snapshot}.tar.xz
# 4 Debian patches
Patch1:		01_fix_out_of_source_build.diff
Patch2:		02_change_desktop_file_installation.diff
Patch3:		03_disable_engine_with_nspluginviewer.diff
Patch4:		04_no_kde4_in_configfile.diff
Patch5:		gtk-qt-engine-1.1-glib.patch
BuildRequires:	cmake
BuildRequires:	kdelibs4-devel
BuildRequires:	kde4-macros
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libbonoboui-2.0)
BuildRequires:	devel(libgcrypt)
Requires:	%{libname} = %{version}-%{release}
Requires:	gtk-qt-kcm

%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt4 widget styles. 

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself. It also adds a configuration tool
to KDE4's System Settings - Appearance which let you change the theme
of GTK+ applications in KDE.

This theme engine is currently experimental and considered as an ugly hack
by some people. Use at your own risk.

%package -n %{libname}
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	gtk-qt-engine < 1.1-3

%description -n %{libname}
Dynamic libraries for %{name}.

%package -n gtk-qt-kcm
Summary:	KDE System Settings module to configure GTK+ 2 theme
Group:		Graphical desktop/KDE
Conflicts:	gtk-qt-engine < 1.1-5

%description -n gtk-qt-kcm
This package provides configuration module to configure GTK+ 2.x styles from
within Systemsettings -> "Application Appearance" in KDE4.

%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%cmake_kde4
%make

%install
%makeinstall_std -C build

# fix .desktop file categories to make the kcm module show up under "Application
#  Appearance" in systemsettings
sed -i 's/X-KDE-System-Settings-Parent-Category=appearance/X-KDE-System-Settings-Parent-Category=application-appearance/' \
%{buildroot}%{_kde_services}/kcmgtk4.desktop

%find_lang kcmgtk4

%files
%doc AUTHORS ChangeLog
%{_datadir}/themes/Qt4/gtk-2.0/gtkrc

%files -n %{libname}
%{_libdir}/gtk-2.0/*/engines/libqt4engine.so

%files -n gtk-qt-kcm -f kcmgtk4.lang
%{_kde_iconsdir}/kcmgtk.png
%{_kde_libdir}/kde4/kcm_gtk4.so
%{_kde_services}/kcmgtk4.desktop


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1-5.r5.4mdv2011.0
+ Revision: 664946
- mass rebuild

* Tue Dec 21 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.1-5.r5.3mdv2011.0
+ Revision: 623728
- rename systemsettings-qt-gtk to gtk-qt-kcm (and change package description a bit)
- fix the .desktop file categories to make it show up under "Application Appearance"
  in systemsettings
- sync the 01_fix_out_of_source_build patch from Debian, this changes the
  translations filenames from gtkqtengine.mo to kcmgtk4.mo to make them work

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-5.r5.2mdv2011.0
+ Revision: 610997
- rebuild

* Fri Nov 13 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1-5.r5.1mdv2010.1
+ Revision: 465801
- Update to svn snapshot in order to fix bugs in 1.1
- Sync Debian patches
- Move the KDE System Settings module to configure the GtK+ theme in
  KDE to a separate subpackage because it is useful without gtk-qt-engine
- Add a warning to the gtk-engine package because of the experimental
  nature of this engine.
- Various SPEC file clean-ups

* Sun Aug 09 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1-4mdv2010.0
+ Revision: 413312
-Rebuild

* Sat Aug 02 2008 Frederik Himpe <fhimpe@mandriva.org> 1.1-3mdv2009.0
+ Revision: 260871
- Remove patch to transform it to an application instead of a service
  and instead move the desktop file to the services directory
- Add patch which fixes out of source tree build
- Use %%cmake_kde4 macro for configuration
- Mention configuration panel in System Settings
- Put GTK+ engine in lib package, so that 64 and 32 bits versions can
  be installed together

* Sat Aug 02 2008 Funda Wang <fwang@mandriva.org> 1.1-2mdv2009.0
+ Revision: 260615
- rediff patch0 and patch1
- clearify the license

* Sat Aug 02 2008 Funda Wang <fwang@mandriva.org> 1.1-1mdv2009.0
+ Revision: 260572
- Switch to kde4 version 1.1

* Thu Jun 19 2008 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 0.8-5mdv2009.0
+ Revision: 226072
- Move to /opt

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 04 2008 Frederik Himpe <fhimpe@mandriva.org> 0.8-4mdv2008.1
+ Revision: 162432
- Fix Flash plug-in in Konqueror not working if gtk-qt-engine is
  being used (patch1 from Debian:
  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=460634)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 22 2007 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 0.8-3mdv2008.0
+ Revision: 92275
- Do not use NoDisplay for Kcontol kcm

* Wed Sep 19 2007 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 0.8-2mdv2008.0
+ Revision: 90495
- [BUGFIX] D not show on the menu (Bug #33662)

* Fri Aug 31 2007 Funda Wang <fwang@mandriva.org> 0.8-1mdv2008.0
+ Revision: 76480
- fix url and tarball location
- New version 0.8
- Import gtk-qt-engine



* Thu Sep  7 2006 Couriousous <couriousous@mandriva.org> 0.7-2mdv2007.0
- fix #24967

* Tue Aug 22 2006 Couriousous <couriousous@mandriva.org> 0.7-1mdv2007.0
- 0.7

* Mon Jun 12 2006 David Walluck <walluck@mandriva.org> 0.7-0.20060204.1mdv2007.0
- CVS 20060204
- remove black menu patch (fixed upstream)
- rebuild for new gtk

* Sat Sep 10 2005 Couriousous <couriousous@mandriva.org> 0.7-0.20050303.3mdk
- Patch0: fix black menu #18423 (patch from ubuntu, thanks to Frederik Himpe)
- Patch1: fix compile on x86_64
- Do not add -pipe option to gcc, it fail for an unknow reason

* Thu Mar 17 2005 Nicolas Lécureuil <neoclust@mandrake.org> 0.7-0.20050303.2mdk
- Fix compile For arch64 From trem

* Thu Mar 03 2005 Couriousous <couriousous@mandrake.org> 0.7-0.20050303.1mdk
- Sync with cvs ( fix #14064 )

* Mon Jan 31 2005 Couriousous <couriousous@mandrake.org> 0.7-0.20050131.1mdk
- Sync with cvs
- Take some fix from Pascal Billery-Schneider <sagittarius@jabber.org> spec

* Sun Jan 30 2005 Couriousous <couriousous@mandrake.org> 0.6-1mdk
- First Mandrakelinux release
