Name:           smesh
Version:        5.1.2.2
Release:        2.svn54%{?dist}
Summary:        OpenCascade based MESH framework

# This library is LGPLv2+ but links against the non-free library OCE.
License:        GPLv2 with exception
URL:            https://sourceforge.net/projects/salomesmesh

# Source is svn checkout since the last release is too old:
# https://salomesmesh.svn.sourceforge.net/svnroot/salomesmesh/trunk
Source0:        smesh-5.1.2.2-svn54.tar.gz

# Patch emailed upstream to Fotios Sioutis <sfotis@gmail.com>
# on 12/21/11.
Patch0:         smesh.patch
Patch1:         smesh-cmake_fixes.patch

BuildRequires:  cmake doxygen
BuildRequires:  OCE-devel
BuildRequires:  boost-devel
BuildRequires:  gcc-gfortran
BuildRequires:  f2c
BuildRequires:  dos2unix


%description
A complete OpenCascade based MESH framework.


%package doc
Summary:        Development documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Development documentation for %{name}.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files and headers for %{name}.


%prep
%setup -q -c %{name}-%{version}
%patch0 -p1
%patch1 -p1 -b .cmakefix

dos2unix -k LICENCE.lgpl.txt


%build
rm -rf build && mkdir build && pushd build
LDFLAGS='-Wl,--as-needed'; export LDFLAGS
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DOCC_INCLUDE_PATH=%{_includedir}/oce \
       ..

make %{?_smp_mflags}

# Build documentation
make doc
popd

# Remove install script since we don't need it.
rm -f doc/html/installdox


%install
pushd build
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc LICENCE.lgpl.txt
%{_libdir}/*.so.*

%files doc
%doc doc/html

%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Thu Jan 19 2012 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-2.svn54
- Minor updates to spec file.

* Tue Dec 20 2011 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-1.svn54
- Initial release.
