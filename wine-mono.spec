%undefine _hardened_build
%{?mingw_package_header}

Name:           wine-mono
Version:        4.9.4
Release:        2%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
URL:            http://wiki.winehq.org/Mono
Source0:        http://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}.tar.gz
# to statically link in winpthreads
Patch0:         wine-mono-build-static.patch
# update from python2 to python3
Patch1:         python3.patch

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    %{power64} s390x s390

# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-crt
BuildRequires:  mingw64-winpthreads-static
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-crt
BuildRequires:  mingw32-winpthreads-static

BuildRequires:  autoconf automake
BuildRequires:  bc
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  wine-core
BuildRequires:  /usr/bin/python
BuildRequires:  /usr/bin/pathfix.py

Requires: wine-filesystem

# Bundles FAudio, libtheorafile, libmojoshader, SDL2, SDL2_image

%description
Windows Mono library required for Wine.

%global mingw_build_win32 0
%global debug_package %{nil}
%global mingw_debug_package %{nil}
%{?mingw_debug_package}

%prep
%setup -q
%patch0 -p1 -b.static
%patch1 -p1

# Fix all Python shebangs
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
sed -i 's/GENMDESC_PRG=python/GENMDESC_PRG=python3/' mono/mono/mini/Makefile.am.in

%build
make %{_smp_mflags} image

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}/
cp -rp image/* \
    %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}/

# prep licenses
cp mono/LICENSE mono-LICENSE
cp mono/COPYING.LIB mono-COPYING.LIB
cp mono/mcs/COPYING mono-mcs-COPYING

pushd mono/mcs

for l in `ls LICENSE*`; do
echo $l
cp $l ../../mono-mcs-$l
done

popd

cp mono-basic/README mono-basic-README
cp mono-basic/LICENSE mono-basic-LICENSE

%files
%license COPYING mono-LICENSE mono-COPYING.LIB mono-basic-LICENSE mono-mcs*
%doc README mono-basic-README
%{_datadir}/wine/mono/wine-mono-%{version}/

%changelog
* Sat Oct 10 2020 Zhiyi Weng <zhiyi@iscas.ac.cn> - 4.9.4-2
- Initial version.
