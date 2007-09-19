%define name	gtk-qt-engine
%define version	0.8
%define release	%mkrel 2

Summary:	Allow GTK to use Qt widget styles
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://gtk-qt.ecs.soton.ac.uk/files/%{version}/%{name}-%{version}.tar.bz2
Patch0:		gtk-qt-engine-fix-menuentry.patch	
License:	GPL
Group:		Graphical desktop/Other
Url:		http://gtk-qt.ecs.soton.ac.uk/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk2-devel
BuildRequires:	qt3-devel
BuildRequires:	kdebase-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	bonoboui-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt widget styles. 

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
cmake . \
    %if "lib" != "lib" 
        -DLIB_SUFFIX=64 \
    %endif 
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_STATIC_LIBS:BOOL=OFF
make

%install
rm -rf %{buildroot}
%makeinstall_std

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
%{_datadir}/applications/*.desktop
%{_datadir}/themes/Qt/gtk-2.0/gtkrc
%{_libdir}/kde3/*
%{_libdir}/gtk-2.0/*/engines/*
