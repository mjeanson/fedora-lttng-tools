
Name:           lttng-tools
Version:        2.4.1
Release:        3%{?dist}
License:        GPLv2 and LGPLv2
URL:            http://lttng.org/lttng2.0
Group:          Development/Tools
Summary:        LTTng control and utility programs
Source0:        http://lttng.org/files/lttng-tools/%{name}-%{version}.tar.bz2
Source1:        lttng-sessiond.service

BuildRequires:  libuuid-devel popt-devel libtool systemd-units
BuildRequires:  lttng-ust-devel >= 2.3
BuildRequires:  userspace-rcu-devel >= 0.7.2
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

#GCC crash when building this package on arm with hardening activated (See bug 987192).
%ifnarch %{arm}
%global _hardened_build 1
%endif

%description
This package provides the unified interface to control both the LTTng kernel
and userspace (UST) tracers.

%package -n %{name}-devel
Summary:        LTTng control and utility library (development files)
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
This package provides the development files to
implement trace control in external applications

%prep
%setup -q

%build
#automake version change
autoreconf -vfi
#Reinitialize libtool with the fedora version to remove Rpath
libtoolize -cvfi

%configure --disable-static

make %{?_smp_mflags} V=1

%check
# tests are currently broken for this latest release
# see upstream bug: http://bugs.lttng.org/issues/287
#make check

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la
install -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/lttng-sessiond.service
# Install upstream bash auto completion for lttng
install -D -m644 extras/lttng-bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/lttng

%pre
getent group tracing >/dev/null || groupadd -r tracing
exit 0

%post
/sbin/ldconfig
%systemd_post lttng-sessiond.service

%preun
%systemd_preun lttng-sessiond.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart lttng-sessiond.service 

%files
%dir %{_libdir}/lttng
%dir %{_libdir}/lttng/libexec
%{_bindir}/lttng
%{_libdir}/lttng/libexec/lttng-consumerd
%{_bindir}/lttng-sessiond
%{_bindir}/lttng-relayd
%{_libdir}/*.so.*
%{_mandir}/man1/lttng.1.gz
%{_mandir}/man8/lttng-sessiond.8.gz
%{_mandir}/man8/lttng-relayd.8.gz
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/*.txt
%doc README
%{_unitdir}/lttng-sessiond.service
%{_sysconfdir}/bash_completion.d/


%files -n %{name}-devel
%{_prefix}/include/lttng/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ctl.pc

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.4.1-1
- New upstream release

* Sat Feb 22 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-3
- Rebuilt for URCU soname bump

* Tue Sep 24 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-2
- Disable hardening flags on arm, since it does not build with them

* Fri Sep 20 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.3-1
- New upstream bugfix version

* Mon Jul 22 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.2-1
- New upstream bugfix version

* Tue Jul 16 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.1-1
- New upstream version

* Fri May 17 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-2
- Add hardening option (#955452)
- Use new systemd-rpm macros (#850195)

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-1
- New upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-1
- New upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 07 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.3-1
- New upstream version and updates from review comments 

* Tue Jun 19 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.2-1
- New package, inspired by the one from OpenSuse

