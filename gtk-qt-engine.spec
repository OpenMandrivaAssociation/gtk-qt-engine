%define libname %mklibname gtk-qt-engine
%define snapshot r5

Summary:	Allow GTK to use Qt widget styles
Name:		gtk-qt-engine
Version:	1.1
Release:	%mkrel 5.%{snapshot}.3
Source0:	http://gtk-qt.ecs.soton.ac.uk/files/%{version}/%{name}-%{version}-%{snapshot}.tar.xz
# Debian patches
Patch1:		01_fix_out_of_source_build.diff
Patch2:		02_change_desktop_file_installation.diff
Patch3:		03_disable_engine_with_nspluginviewer.diff
Patch4:		04_no_kde4_in_configfile.diff
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		http://gtk-qt.ecs.soton.ac.uk/
BuildRequires:	gtk2-devel
BuildRequires:	kdelibs4-devel
BuildRequires:	kde4-macros
BuildRequires:	cmake
BuildRequires:	bonoboui-devel
Requires:	%{libname} = %{version}
Requires:	gtk-qt-kcm
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt4 widget styles. 

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself. It also adds a configuration tool
to KDE4's System Settings - Appearance which let you change the theme
of GTK+ applications in KDE.

This theme engine is currently experimental and considered as an ugly hack
by some people. Use at your own risk.

%package -n %{libname}
Summary:        Dynamic libraries for %{name}
Group:          System/Libraries
Requires:       %{name} = %{version}
Conflicts:	gtk-qt-engine < 1.1-3

%description -n %{libname}
Dynamic libraries for %{name}.

%package -n gtk-qt-kcm
Summary:	KDE System Settings module to configure GTK+ 2 theme
Group:		Graphical desktop/KDE
Conflicts:	gtk-qt-engine < 1.1-5
Obsoletes:	systemsettings-qt-gtk

%description -n gtk-qt-kcm
This package provides configuration module to configure GTK+ 2.x styles from
within Systemsettings -> "Application Appearance" in KDE4.

%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%cmake_kde4
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

# fix .desktop file categories to make the kcm module show up under "Application
#  Appearance" in systemsettings
sed -i 's/X-KDE-System-Settings-Parent-Category=appearance/X-KDE-System-Settings-Parent-Category=application-appearance/' \
%{buildroot}%{_kde_services}/kcmgtk4.desktop

%find_lang kcmgtk4

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{_datadir}/themes/Qt4/gtk-2.0/gtkrc

%files -n %libname
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/engines/libqt4engine.so

%files -n gtk-qt-kcm -f kcmgtk4.lang
%defattr(-,root,root)
%{_kde_iconsdir}/kcmgtk.png
%{_kde_libdir}/kde4/kcm_gtk4.so
%{_kde_services}/kcmgtk4.desktop
