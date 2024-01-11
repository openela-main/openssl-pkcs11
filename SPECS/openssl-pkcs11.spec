Version: 0.4.10
Release: 3%{?dist}

# Define the directory where the OpenSSL engines are installed
%global enginesdir %{_libdir}/engines-1.1

Name:           openssl-pkcs11
Summary:        A PKCS#11 engine for use with OpenSSL
# The source code is LGPLv2+ except eng_back.c and eng_parse.c which are BSD
License:        LGPLv2+ and BSD
URL:            https://github.com/OpenSC/libp11
Source0:        https://github.com/OpenSC/libp11/releases/download/libp11-%{version}/libp11-%{version}.tar.gz

Patch0:         openssl-pkcs11-0.4.10-small-bug-fixes.patch
Patch1:         openssl-pkcs11-0.4.10-search-objects-in-all-matching-tokens.patch
Patch2:         openssl-pkcs11-0.4.10-set-rsa-fips-method-flag.patch
Patch3:         openssl-pkcs11-0.4.10-fix-memory-leak.patch
Patch4:         openssl-pkcs11-0.4.10-fix-potential-leak-in-rsa-method.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  openssl-devel
BuildRequires:  openssl >= 1.0.2
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(p11-kit-1)
# Needed for testsuite
BuildRequires:  softhsm opensc procps-ng

%if 0%{?fedora}
BuildRequires:  doxygen
%endif

Requires:       p11-kit-trust
Requires:       openssl >= 1.0.2

# Package renamed from libp11 to openssl-pkcs11 in release 0.4.7-4
Provides:       libp11%{?_isa} = %{version}-%{release}
Obsoletes:      libp11 < 0.4.7-4
# The engine_pkcs11 subpackage is also provided 
Provides:       engine_pkcs11%{?_isa} = %{version}-%{release}
Obsoletes:      engine_pkcs11 < 0.4.7-4

%if 0%{?fedora}
# The libp11-devel subpackage was removed in libp11-0.4.7-1, but not obsoleted
# This Obsoletes prevents the conflict in updates by removing old libp11-devel
Obsoletes:      libp11-devel < 0.4.7-4
%endif

%description -n openssl-pkcs11
openssl-pkcs11 enables hardware security module (HSM), and smart card support in
OpenSSL applications. More precisely, it is an OpenSSL engine which makes
registered PKCS#11 modules available for OpenSSL applications. The engine is
optional and can be loaded by configuration file, command line or through the
OpenSSL ENGINE API.

# The libp11-devel subpackage was reintroduced in libp11-0.4.7-7 for Fedora
%if 0%{?fedora}
%package -n libp11-devel
Summary:        Files for developing with libp11
Requires:       %{name} = %{version}-%{release}

%description -n libp11-devel
The libp11-devel package contains libraries and header files for
developing applications that use libp11.

%endif

%prep
%autosetup -p 1 -n libp11-%{version}

%build
autoreconf -fvi
export CFLAGS="%{optflags}"
%if 0%{?fedora}
%configure --disable-static --enable-api-doc --with-enginesdir=%{enginesdir}
%else
%configure --disable-static --with-enginesdir=%{enginesdir}
%endif
make V=1 %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{enginesdir}
make install DESTDIR=%{buildroot}

# Remove libtool .la files
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{enginesdir}/*.la

%if ! 0%{?fedora}
## Remove development files
rm -f %{buildroot}%{_libdir}/libp11.so
rm -f %{buildroot}%{_libdir}/pkgconfig/libp11.pc
rm -f %{buildroot}%{_includedir}/*.h
%endif

# Remove documentation automatically installed by make install
rm -rf %{buildroot}%{_docdir}/libp11/

%check
make check %{?_smp_mflags} || if [ $? -ne 0 ]; then cat tests/*.log; exit 1; fi;

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libp11.so.*
%{enginesdir}/*.so

%if 0%{?fedora}
%files -n libp11-devel
%doc examples/ doc/api.out/html/
%{_libdir}/libp11.so
%{_libdir}/pkgconfig/libp11.pc
%{_includedir}/*.h
%endif

%changelog
* Mon Jan 09 2023 Clemens Lang <cllang@redhat.com> - 0.4.10-3
- Fix memory leak in PKCS11_pkey_meths (#2097690)
- Fix memory leak in RSA method (#2097690)

* Thu Nov 28 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-2
- Set RSA_FLAG_FIPS_METHOD for RSA methods (#1777892)

* Thu Nov 21 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-1
- Update to 0.4.10 (#1745082)
- Add BuildRequires for OpenSSL >= 1.0.2, required for testing
- Print tests logs if failed during build
- Small bug fixes such as removal of unused variable
- Search objects in all matching tokens (#1705505)

* Tue Sep 18 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.8-2
- Require OpenSSL >= 1.0.2
- Fixed missing declaration of ERR_get_CKR_code()
- Add support to use EC keys and tests (#1625338)
- Exposed check_fork() API
- Fixed memory leak of RSA objects in pkcs11_store_key()
- Updated OpenSSL license in eng_front.c
- Fixed build for old C dialects
- Allow engine to use private key without PIN
- Require DEBUG to be defined to print debug messages
- Changed package description

* Mon Aug 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.8-1
- Update to 0.4.8-1
- RSA key generation on the token
- RSA-OAEP and RSA-PKCS encryption support
- RSA-PSS signature support
- Support for OpenSSL 1.1.1 beta
- Removed support for OpenSSL 0.9.8
- Various bug fixes and enhancements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-7
- Reintroduce libp11-devel subpackage to Fedora (#1583719)

* Tue Mar 13 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-6
- Obsolete libp11-devel to fix update

* Tue Mar 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-5
- Fixed broken Obsoletes

* Thu Mar 01 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-4
- Package renamed from libp11 to openssl-pkcs11
