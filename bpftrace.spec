%global commit_bpftrace c49b333c034a6d29a7ce90f565e27da1061af971
%global shortcommit_bpftrace %(c=%{commit_bpftrace}; echo ${c:0:7})

Name:           bpftrace
Version:        0.0
Release:        2.20181210git%{shortcommit_bpftrace}%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0

URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/%{commit_bpftrace}.tar.gz

# https://github.com/iovisor/bpftrace/pull/227
Patch0:         %{name}-add-support-to-link-bpftrace-against-the-system-inst.patch
# https://github.com/iovisor/bcc/pull/2022
Patch1:         %{name}-add-extra-headers-from-bcc-package.patch
# https://github.com/iovisor/bpftrace/pull/264
Patch2:         %{name}-install-_example.txt-files-to-tools-doc-they-are-ref.patch

# Arches will be included as upstream support is added and dependencies are
# satisfied in the respective arches
ExclusiveArch:  x86_64 %{power64}

BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  bcc-devel


%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap


%prep
%autosetup -p1 -n bpftrace-%{commit_bpftrace}


%build
%cmake . \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DSYSTEM_BCC_LIBRARY:BOOL=ON \
        -DENABLE_TESTS:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=OFF
make %{?_smp_mflags}


%install
%make_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{name}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{name}\([0-9.]\+\)\?$=#!%{_bindir}/%{name}=' {} \;

# Move man pages to the right location
mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_prefix}/man/* %{buildroot}%{_mandir}/


%files
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tools
%dir %{_datadir}/%{name}/tools/doc
%{_bindir}/%{name}
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{name}/tools/*.bt
%{_datadir}/%{name}/tools/doc/*.txt


%changelog
* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-2.20181210gitc49b333
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181210gitc49b333
- Updated to latest upstream (c49b333c034a6d29a7ce90f565e27da1061af971)

* Wed Nov 07 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181107git029717b
- Initial import
