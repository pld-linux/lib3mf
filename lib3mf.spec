#
# Conditional build:
%bcond_with	tests		# build with tests
#
Summary:	Implementation of the 3D Manufacturing Format file standard
Name:		lib3mf
Version:	2.5.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/3MFConsortium/lib3mf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	43da209fe1b28464ea6f93fb7697d187
Patch0:		fast-float-include-path.patch
URL:		https://3mf.io/
BuildRequires:	cmake
BuildRequires:	libzip-devel
BuildRequires:	ossp-uuid-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
%{?with_tests:BuildRequires:	googletest}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
As 3MF shall become an universal 3D Printing standard, its quick
adoption is very important. This library shall lower all barriers of
adoption to any possible user, let it be software providers, hardware
providers, service providers or middleware tools. The specification
can be downloaded at http://3mf.io/specification/

Its aim is to offer an open source way to integrate 3MF reading and
writing capabilities, as well as conversion and validation tools for
input and output data. The 3MF Library shall provide a clean and
easy-to-use API to speed up the development and keep integration costs
at a minimum.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q
%patch -P0 -p1

%build
mkdir -p build
cd  build
%{cmake} ../ \
		-DUSE_INCLUDED_ZLIB=OFF \
		-DUSE_INCLUDED_LIBZIP=OFF \
		-DUSE_INCLUDED_SSL=OFF \
		-DSTRIP_BINARIES=OFF \
		-DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/lib3MF \
		%{cmake_on_off tests LIB3MF_TESTS}
	%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/lib3mf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib3mf.so.2

%files devel
%defattr(644,root,root,755)
%doc CONTRIBUTING.md
%attr(755,root,root) %{_libdir}/lib3mf.so
%{_includedir}/lib3MF
%{_pkgconfigdir}/lib3mf.pc
%{_libdir}/cmake/lib3mf
