%define name	gtk-qt-engine
%define libname %mklibname gtk-qt-engine
%define version	1.1
%define release	%mkrel 3

Summary:	Allow GTK to use Qt widget styles
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://gtk-qt.ecs.soton.ac.uk/files/%{version}/%{name}-%{version}.tar.bz2
Patch0:         gtk-qt-engine-1.1-fix-desktop-destination.patch
Patch1:		gtk-qt-engine-1.1-fix-kde-nsplugin.patch
Patch2:         gtk-qt-engine-1.1-fix-out-of-source-build.patch
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://gtk-qt.ecs.soton.ac.uk/
BuildRequires:	gtk2-devel
BuildRequires:	kdelibs4-devel
BuildRequires:	kde4-macros
BuildRequires:	cmake
BuildRequires:	bonoboui-devel
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt4 widget styles. 

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself. It also adds a configuration tool
to KDE4's System Settings - Appearance which let you change the theme
of GTK+ applications in KDE.

%package -n %{libname}
Summary:        Dynamic libraries for %{name}
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}
Conflicts:	gtk-qt-engine < 1.1-3

%description -n %{libname}
Dynamic libraries for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .fix-desktop-destination.patch
%patch1 -p1 -b .fix-kde-nsplugin.patch
%patch2 -p1 -b .fix-out-of-source-build.patch

%build
%cmake_kde4
make

%install
rm -rf %{buildroot}
make -C build DESTDIR=%buildroot install

%find_lang gtkqtengine

%clean
rm -rf %{buildroot}

%files -f gtkqtengine.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{_kde_iconsdir}/kcmgtk.png
%{_kde_datadir}/kde4/services/kcmgtk4.desktop
%{_kde_datadir}/themes/Qt4/gtk-2.0/gtkrc
%{_kde_libdir}/kde4/kcm_gtk4.so

%files -n %libname
%{_libdir}/gtk-2.0/*/engines/libqt4engine.so
