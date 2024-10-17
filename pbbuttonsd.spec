%define name pbbuttonsd
%define version 0.7.4
%define release %mkrel 2
%define real_ver 0.7.4

Name: %{name}
Summary: Apple Powerbook power/keyboard daemon
Version: %{version}
Release: %{release}
Source: http://prdownloads.sourceforge.net/pbbuttons/%{name}-%{real_ver}.tar.bz2
Source1: pbbuttonsd.init
Patch0:	 pbbuttonsd-0.6.7-haldaemon.patch.bz2
Patch2:  pbbuttonsd_laptopmode_supermount.patch.bz2
URL: https://pbbuttons.sourceforge.net/
Group: System/Configuration/Hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libalsa-devel glib2-devel
ExclusiveArch: ppc
License: GPL

%description
A special Tool for Apple PowerBook or iBook (TM) owners. It makes
the keys for controlling the brightness and volume work
as expected. It also controls trackpad settings and
power management.

%package devel
Summary:	Include files for pbbuttonsd
Group:		Development/Other
Requires:	%{name} = %{version}

%description devel
pbbuttonsd header files for pbbuttonsd development and client support.

%prep
rm -rf %{buildroot}
%setup -q -n %{name}-%{real_ver}
# (sb) skip backup files or it tried to install them
%patch0 -p1
%patch2 -p1
%build
%configure
%make

%install
install -d %buildroot%{_sysconfdir}
#depends on patch0:
chmod +x scripts/{scripts,event}.d/hal

%makeinstall
install -c -D -m755 %{SOURCE1} %buildroot%{_initrddir}/pbbuttonsd

%clean
rm -rf %{buildroot}

%post
%_post_service pbbuttonsd

%preun
%_preun_service pbbuttonsd

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING README TODO
%{_mandir}/man*/*
%{_bindir}/*
%dir /var/lib/ibam
%lang(ca) %{_datadir}/locale/ca/*
%lang(de) %{_datadir}/locale/de/*
%lang(es) %{_datadir}/locale/es/*
#lang(it) %{_datadir}/locale/it/*

%config(noreplace) %{_sysconfdir}/pbbuttonsd.conf
%config(noreplace) %{_sysconfdir}/power/README

%defattr(0755,root,root)
%config(noreplace) %{_sysconfdir}/power/pmcs*
%config(noreplace) %{_sysconfdir}/power/event.d/*
%config(noreplace) %{_sysconfdir}/power/scripts.d/*
%config(noreplace) %{_initrddir}/pbbuttonsd

%files devel
%defattr(-,root,root,0755)
%{_includedir}/*
%{_libdir}/*

