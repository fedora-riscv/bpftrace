Name:           bpftrace
Version:        0.11.0
Release:        2%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0

URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Arches will be included as upstream support is added and dependencies are
# satisfied in the respective arches
ExclusiveArch:  x86_64 %{power64} aarch64 s390x

BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  bcc-devel >= 0.11.0-2
BuildRequires:  libbpf-devel
BuildRequires:  libbpf-static
BuildRequires:  binutils-devel


%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap


%prep
%autosetup -p1


%build
%cmake . \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DBUILD_TESTING:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=OFF \
        -DLIBBCC_LIBRARIES:PATH=/usr/lib64/libbcc-no-libbpf.so
%make_build


%install
# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post %{nil}
%global _find_debuginfo_opts -g

%make_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{name}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{name}\([0-9.]\+\)\?$=#!%{_bindir}/%{name}=' {} \;


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
* Tue Aug 04 2020 Augusto Caringi <acaringi@redhat.com> - 0.11.0-2
- Fix 'bpftrace symbols are stripped' #1865787

* Thu Jul 16 2020 Augusto Caringi <acaringi@redhat.com> - 0.11.0-1
* Rebased to version 0.11.0

* Tue May 19 2020 Augusto Caringi <acaringi@redhat.com> - 0.10.0-2
- Rebuilt for new bcc/libbpf versions

* Tue Apr 14 2020 Augusto Caringi <acaringi@redhat.com> - 0.10.0-1
- Rebased to version 0.10.0
- Dropped support for s390x temporaly due to build error

* Thu Feb 06 2020 Augusto Caringi <acaringi@redhat.com> - 0.9.4-1
- Rebased to version 0.9.4

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.3-1
- Rebased to version 0.9.3

* Thu Aug 01 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.2-1
- Rebased to version 0.9.2

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.1-1
- Rebased to version 0.9.1

* Thu Apr 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-3
- Rebuilt for bcc 0.9.0

* Mon Apr 22 2019 Neal Gompa <ngompa@datto.com> - 0.9-2
- Fix Source0 reference
- Use make_build macro for calling make

* Mon Apr  1 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.9-1
- Build on aarch64 and s390x

* Mon Mar 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-0
- Updated to version 0.9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-2.20181210gitc49b333
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181210gitc49b333
- Updated to latest upstream (c49b333c034a6d29a7ce90f565e27da1061af971)

* Wed Nov 07 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181107git029717b
- Initial import
