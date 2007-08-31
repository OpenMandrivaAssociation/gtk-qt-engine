%define __libtoolize	/bin/true
%define __cputoolize	/bin/true

%define name	gtk-qt-engine
%define version	0.7
%define release	%mkrel 2

%define gtk_version %(pkg-config --variable=gtk_binary_version gtk+-2.0)

Summary:	Allow GTK to use Qt widget styles
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.bz2
License:	GPL
Group:		Graphical desktop/Other
Url:		http://www.freedesktop.org/Software/gtk-qt/
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	gtk2-devel
BuildRequires:	qt3-devel
BuildRequires:	kdebase-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt widget styles. 

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself.

%prep
%setup -q -n %{name}

%build

%if %{_lib} == "lib64"
%configure2_5x --disable-rpath --enable-final --enable-libsuffix=64
%else
%configure2_5x --disable-rpath --enable-final
%endif
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%{__perl} -pi -e 's|section="([^"]+)"|section="System/Configuration/KDE/LookNFeel" xdg="true" |' %{buildroot}/%{_menudir}/kcmgtk.menu
%{__perl} -pi -e "s|local.kcmgtk|%{name}|" %{buildroot}/%{_menudir}/kcmgtk.menu
%{__perl} -pi -e "s|kcmshell kcmgtk|kcmshell \"GTK styles and fonts\"|" %{buildroot}/%{_datadir}/applnk/Settings/LookNFeel/kcmgtk.desktop
%{__perl} -pi -e "s|kcmshell kcmgtk|kcmshell 'GTK styles and fonts'|" %{buildroot}/%{_menudir}/kcmgtk.menu
%{__mv} %{buildroot}/%{_menudir}/kcmgtk.menu %{buildroot}/%{_menudir}/%{name}

%{__rm} -f %{buildroot}/%{_datadir}/applications/kcmgtk-xdg.desktop

%find_lang gtkqtengine

%post 
%{update_menus} 

%postun 
%{clean_menus}

%clean
rm -rf %{buildroot}

%files -f gtkqtengine.lang
%defattr(-,root,root)
%doc README
%{_datadir}/applnk/Settings/LookNFeel/kcmgtk.desktop
%{_datadir}/gtk-qt-engine/kde-index.theme
%{_datadir}/themes/Qt/gtk-2.0/gtkrc
%{_menudir}/%{name}
%{_libdir}/kde3/*
%{_libdir}/gtk-2.0/%{gtk_version}/engines/*
