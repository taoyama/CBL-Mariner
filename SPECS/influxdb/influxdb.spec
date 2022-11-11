Name:           influxdb2
Summary:        Scalable datastore for metrics, events, and real-time analytics
License:        MIT
Group:          Productivity/Databases/Servers
Version:        2.4.0
Release:        %1{?dist}
URL:            https://github.com/influxdata/influxdb
Source:         %{URL}/archive/refs/tags/v%{version}.tar.gz
Source1:        influxdb.service
Source2:        influxdb.tmpfiles
Source3:        influxdb-user.conf
Source4:        config.yaml
Source99:       vendor.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  sysuser-tools
%{sysusers_requires}
BuildRequires:  fdupes
BuildRequires:  go >= 1.18
BuildRequires:  golang-packaging >= 15.0.8
BuildRequires:  systemd-rpm-macros
BuildRequires:  build-essential
BuildRequires:  pkg-config >= 0.171.0
BuildRequires:  protobuf-devel
BuildRequires:  kernel-headers
BuildRequires:  rust
BuildRequires:  clang
BuildRequires:  tzdata
BuildRequires:  git

%{!?_tmpfilesdir:%global _tmpfilesdir /usr/lib/tmpfiles.d}
%{systemd_requires}
Requires(post): systemd

%description
InfluxDB is an distributed time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%package        devel
Summary:        InfluxDB development files
Group:          Development/Languages/Golang
Requires:       go
Requires:       tzdata

%description devel
Go sources and other development files for InfluxDB

%prep
%setup -q
%setup -q -T -D -a 99

%build
export GO111MODULE=on

# Build influxdb
%goprep github.com/influxdata/influxdb/v2
%gobuild -mod=vendor -ldflags="-X main.version=%{version}" cmd/...

%sysusers_generate_pre %{SOURCE3} %{name}

%install
%gosrc
%fdupes -s %{buildroot}/%{go_contribsrcdir}/github.com/influxdata/influxdb

mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
mkdir -p %{buildroot}%{_localstatedir}/lib/influxdb
mkdir -p %{buildroot}%{_sbindir}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/influxdb.service
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rcinfluxdb
install -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/influxdb.conf
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/influxdb-user.conf
install -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/influxdb2/config.yaml
install -D -m 0755 -t %{buildroot}%{_bindir} %{_builddir}/go/bin/*

%check
#%%gotest github.com/influxdata/influxdb

%pre -f %{name}.pre
%service_add_pre influxdb.service

%preun
%service_del_preun influxdb.service

%post
%tmpfiles_create %_tmpfilesdir/influxdb.conf
%service_add_post influxdb.service

%postun
%service_del_postun influxdb.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%dir %{_sysconfdir}/influxdb2
%config(noreplace) %{_sysconfdir}/influxdb2/config.yaml
%{_bindir}/influxd
%{_bindir}/telemetryd
%{_sbindir}/rcinfluxdb
%{_unitdir}/influxdb.service
%{_datadir}/influxdb2
%{_sysusersdir}/influxdb-user.conf
%dir %{_tmpfilesdir}
%{_tmpfilesdir}/influxdb.conf
%attr(0755, influxdb, influxdb) %dir %{_localstatedir}/log/influxdb
%attr(0755, influxdb, influxdb) %dir %{_localstatedir}/lib/influxdb

%files devel
%license LICENSE
%dir %{go_contribsrcdir}/github.com
%dir %{go_contribsrcdir}/github.com/influxdata
%{go_contribsrcdir}/github.com/influxdata/influxdb

%changelog