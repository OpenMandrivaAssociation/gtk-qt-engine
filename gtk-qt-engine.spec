%define name	gtk-qt-engine
%define version	1.1
%define release	%mkrel 2

Summary:	Allow GTK to use Qt widget styles
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://gtk-qt.ecs.soton.ac.uk/files/%{version}/%{name}-%{version}.tar.bz2
Patch0:		gtk-qt-engine-1.1-fix-menuentry.patch
Patch1:		gtk-qt-engine-1.1-fix-kde-nsplugin.patch
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://gtk-qt.ecs.soton.ac.uk/
BuildRequires:	gtk2-devel
BuildRequires:	kdelibs4-devel
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
%patch1 -p1

%build
%setup_compile_flags
cmake . \
    %if "%{_lib}" != "lib"
        -DLIB_SUFFIX=64 \
    %endif
    -DCMAKE_INSTALL_PREFIX:PATH=%{_kde_prefix} \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_STATIC_LIBS:BOOL=OFF
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang gtkqtengine

%if %mdkversion < 200900
%post 
%{update_menus} 
%endif

%if %mdkversion < 200900
%postun 
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files -f gtkqtengine.lang
%defattr(-,root,root)
%{_kde_libdir}/kde4/*
%{_libdir}/gtk-2.0/*/engines/*.so
%{_kde_datadir}/applications/kde4/*.desktop
%{_kde_iconsdir}/kcmgtk.png
%{_datadir}/themes/Qt4/gtk-2.0/gtkrc
