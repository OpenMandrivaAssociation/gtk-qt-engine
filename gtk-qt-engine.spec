%define libname %mklibname gtk-qt-engine
%define snapshot r5

Summary:	Allow GTK to use Qt widget styles
Name:		gtk-qt-engine
Version:	1.1
Release:	5.%{snapshot}.8
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
BuildRequires:	pkgconfig(libgcrypt)
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
%setup -qn %{name}
%apply_patches

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

