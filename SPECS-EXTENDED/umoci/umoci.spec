Summary:        Open Container Image manipulation tool
Name:           umoci
Version:        0.4.7
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/opencontainers/umoci
Source0:        https://github.com/opencontainers/umoci/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  golang >= 1.17.9

%description
umoci modifies Open Container images.
umoci is a manipulation tool for OCI images. In particular, it is an
alternative to oci-image-tools provided by the OCI.

%prep
%setup -q

%build
tar --no-same-owner -xf %{SOURCE0}
export GOPATH=%{our_gopath}
make BUILD_FLAGS="-mod=vendor" VERSION="%{version}" umoci

%install
install -D -m 0755 ./umoci %{buildroot}%{_bindir}/umoci

%check
go test -mod=vendor
./umoci --version

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_bindir}/umoci

%changelog
* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-4
- Bump release to rebuild with go 1.19.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.7-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.7-2
- Bump release to rebuild against Go 1.18.5

* Mon Jul 25 2022 Tom Fay <tomfay@microsoft.com> - 0.4.7-1
- Original version for CBL-Mariner.
- License verified.
