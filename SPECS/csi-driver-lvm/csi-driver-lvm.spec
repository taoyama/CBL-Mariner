Summary:        Container storage interface for logical volume management
Name:           csi-driver-lvm
Version:        0.4.1
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/metal-stack/csi-driver-lvm
Source0:        https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2022-09-22 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-govendor.tar.gz vendor
Source1:        %{name}-%{version}-govendor.tar.gz
BuildRequires:  golang
Requires:       %{name}-csi-lvmplugin-provisioner
Requires:       %{name}-lvmplugin

%description
csi-driver-lvm utilizes local storage of Kubernetes nodes to provide persistent storage for pods.

%package csi-lvmplugin-provisioner
Summary:        csi-driver-lvm's csi-lvmplugin-provisioner binary

%description csi-lvmplugin-provisioner
Provisioner of csi driver to utilizes local storage of Kubernetes nodes to provide persistent storage for pods.

%package lvmplugin
Summary:        csi-driver-lvm's lvmplugin binary

%description lvmplugin
lvmplugin collects the size of logical volumes (LV) and free space inside a volume group (VG) from Linux' Logical Volume Manager (LVM).

%prep
%autosetup
%setup -q -T -D -a 1

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m0755 bin/csi-lvmplugin-provisioner %{buildroot}%{_bindir}/
install -D -m0755 bin/lvmplugin %{buildroot}%{_bindir}/

%files

%files csi-lvmplugin-provisioner
%license LICENSE
%doc README.md
%{_bindir}/csi-lvmplugin-provisioner

%files lvmplugin
%license LICENSE
%doc README.md
%{_bindir}/lvmplugin

%changelog
* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.1-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.4.1-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.1-3
- Bump release to rebuild with go 1.18.8

* Tue Sep 27 2022 Lanze Liu <lanzeliu@microsoft.com> - 0.4.1-2
- Split binaries into separate packages

* Thu Sep 23 2022 Lanze Liu <lanzeliu@microsoft.com> - 0.4.1-1
- Original version for CBL-Mariner
- License Verified
