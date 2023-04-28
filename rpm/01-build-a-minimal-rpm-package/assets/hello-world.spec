Name:       hello-world
Version:    0.0.1
Release:    1%{?dist}
Summary:    A simple hello world script
BuildArch:  noarch
License:    GPL
Source0:    %{name}-%{version}.tar.gz
Requires:   bash

%description
Hello world bash script to train building RPM packages.

%prep
%setup -q

%build
# Bash script does not need to build.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
install -m 755 %{name}.sh %{buildroot}%{_bindir}/hello-world

%files
%{_bindir}/%{name}

%changelog
* Sun Jan  01 2023 Joseba Martos <name@example.com> - 0.0.1
- First release to be packaged
