# Use a newer version of cmake on EL.
%if 0%{?rhel}
%global cmake %cmake28
%endif

%global svnrev 55

Name:           smesh
Version:        5.1.2.2
Release:        8.svn%{svnrev}%{?dist}
Summary:        OpenCascade based MESH framework

# This library is LGPLv2+ but links against the non-free library OCE.
License:        GPLv2 with exception
URL:            https://sourceforge.net/projects/salomesmesh

# Source is svn checkout since the last release is too old:
# https://salomesmesh.svn.sourceforge.net/svnroot/salomesmesh/trunk
Source0:        %{name}-%{version}.svn%{svnrev}.tar.gz

# Patch emailed upstream to Fotios Sioutis <sfotis@gmail.com>
# on 12/21/11.
Patch0:         smesh.patch
Patch1:         smesh-cmake_fixes.patch
Patch2:         smesh-5.1.2.2-rm_f2c.patch
Patch3:         smesh-5.1.2.2-pi_to_m_pi.patch
# http://tracker.dev.opencascade.org/view.php?id=23487
Patch4:         smesh-OCE_0.13_port.patch

%if 0%{?rhel}
BuildRequires:  cmake28
%else
BuildRequires:  cmake
%endif
BuildRequires:  doxygen graphviz
BuildRequires:  OCE-devel
BuildRequires:  boost-devel
BuildRequires:  gcc-gfortran
# Do we need this?
#BuildRequires:  f2c f2c-devel
BuildRequires:  dos2unix


%description
A complete OpenCascade based MESH framework.

NOTE: Fortran support (f2c) has been disabled. If it is needed please open a
bug against the smesh component  at: http://bugzilla.rpmfusion.org


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
%setup -q -n %{name}-%{version}.svn%{svnrev}
%patch0 -p1
%patch1 -p1 -b .cmakefix
%patch2 -p1 -b .f2c
%patch3 -p1 -b .pi
%patch4 -p1 -b .oce-0.13

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
* Thu Oct 10 2013 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-8.svn55
- Rebuild for OCE-0.13.

* Mon Jul 15 2013 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-7.svn55
- Rebuild for updated OCE.

* Fri Jun 21 2013 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-6.svn55
- Rebuild for OCE 0.12.

* Fri Feb 15 2013 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-1.svn55
- Update for compatibility with new OCE.

* Mon Oct 22 2012 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-5.svn54
- Remove build requirement for fortran (f2c).
- Initial packaging for EPEL 6.

* Wed Sep 26 2012 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-4.svn54
- Rebuild due to package not being signed in F-18 repo.

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.1.2.2-3.svn54
- Rebuilt for c++ ABI breakage

* Thu Jan 19 2012 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-2.svn54
- Minor updates to spec file.

* Tue Dec 20 2011 Richard Shaw <hobbes1069@gmail.com> - 5.1.2.2-1.svn54
- Initial release.
