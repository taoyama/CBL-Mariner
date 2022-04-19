Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.26
Release:        9%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.aleksey.com/xmlsec/
Source0:        %{url}/download/older-releases/%{name}-%{version}.tar.gz
BuildRequires:  libltdl-devel
BuildRequires:  libxml2-devel
Requires:       libltdl
Requires:       libxml2
Requires:       openssl
Provides:       %{name}-openssl = %{version}-%{release}

%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary:        Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libltdl-devel
Requires:       libxml2-devel
Requires:       openssl-devel
Provides:       %{name}-openssl-devel = %{version}-%{release}

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%prep
%autosetup

%build
%configure \
    --disable-static \
    --with-openssl \
    --without-gcrypt \
    --without-gnutls \
    --without-nss 
%make_build

%install
%make_install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%license COPYING
%{_libdir}/libxmlsec1.so.1*
%{_libdir}/libxmlsec1-openssl.so.1*
%{_bindir}/xmlsec1

%files devel
%defattr(-, root, root)
%{_libdir}/libxmlsec1.so
%{_libdir}/libxmlsec1-openssl.so
%{_bindir}/xmlsec1-config
%{_includedir}/xmlsec1/xmlsec/*.h
%{_includedir}/xmlsec1/xmlsec/private/*.h
%{_includedir}/xmlsec1/xmlsec/openssl/*.h
%{_libdir}/pkgconfig/xmlsec1.pc
%{_libdir}/pkgconfig/xmlsec1-openssl.pc
%{_libdir}/xmlsec1Conf.sh
%{_docdir}/xmlsec1/*
%{_datadir}/aclocal/xmlsec1.m4
%{_mandir}/man1/xmlsec1.1.gz
%{_mandir}/man1/xmlsec1-config.1.gz

%changelog
* Tue Apr 19 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.26-9
- Remove support for gnutls, libgcrypt, nss (and corresponding provides)
- Move unversioned shared libraries to the devel subpackage
- Remove libtool archive files from packaging
- Lint spec

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.26-8
- Add nss as an explicit requirement.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.2.26-7
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.2.26-6
- Enable gcrypt and gnutls support and add explicit provides.

* Sat May 09 00:21:10 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.2.26-5
- Added %%license line automatically

* Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.2.26-4
- License verified.
- Fixed Source0 tag.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.26-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.26-2
- Fix requires.

* Mon Jul 02 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
- Initial version
