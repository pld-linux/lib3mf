# TODO: system cpp-base64?
#
# Conditional build:
%bcond_with	tests		# test suite
#
Summary:	Implementation of the 3D Manufacturing Format file standard
Summary(pl.UTF-8):	Implementacja standardu plików 3D Manufacturing Format
Name:		lib3mf
Version:	2.5.0
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/3MFConsortium/lib3mf/releases
Source0:	https://github.com/3MFConsortium/lib3mf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	43da209fe1b28464ea6f93fb7697d187
Patch0:		%{name}-includes.patch
Patch1:		cmake.patch
Patch2:		pkgconfig.patch
URL:		https://3mf.io/
BuildRequires:	cmake >= 3.10
BuildRequires:	fast_float-devel >= 6.0.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libzip-devel >= 1.10.1
BuildRequires:	libuuid-devel
%{?with_tests:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRequires:	zlib-devel >= 1.3.1
%{?with_tests:BuildRequires:	googletest >= 1.14.0}
Requires:	libzip >= 1.10.1
Requires:	zlib >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
As 3MF shall become an universal 3D Printing standard, its quick
adoption is very important. This library shall lower all barriers of
adoption to any possible user, let it be software providers, hardware
providers, service providers or middleware tools. The specification
can be downloaded at <http://3mf.io/specification/>.

Its aim is to offer an open source way to integrate 3MF reading and
writing capabilities, as well as conversion and validation tools for
input and output data. The 3MF Library shall provide a clean and
easy-to-use API to speed up the development and keep integration costs
at a minimum.

%description -l pl.UTF-8
Jako że 3MF powinien stać się uniwersalnym standardem wydruków 3D,
ważna jest jego szybka adopcja. Ta biblioteka powinna obniżyć bariery
w adopcji u wszystkich możliwych użytkowników, w tym dostawców
oprogramowania, sprzętu, usług czy narzędzi warstwy pośredniej.
Specyfikację można pobrać pod <http://3mf.io/specification/>.

Celem jest zaoferowanie kodu o otwartych źródłach, pozwalającego na
zintegrowanie odczytu i zapisu 3MF, a także narzędzi do konwersji i
sprawdzania poprawności danych wejściowych i wyjściowych. Biblioteka
3MF powinna dostarczyć czyste i łatwe w użyciu API, przyspieszające
rozwój oprogramowania i minimalizujące koszty integracji.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fast_float-devel >= 6.0.0
Requires:	libstdc++-devel >= 6:7
Requires:	libzip-devel >= 1.10.1
Requires:	zlib-devel >= 1.3.1

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%{__rm} -r Libraries/{fast_float,googletest,libressl,libzip,zlib}

%build
mkdir -p build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/lib3MF \
	-DLIB3MF_TESTS=%{__ON_OFF tests} \
	-DSTRIP_BINARIES=OFF \
	-DUSE_INCLUDED_FASTFLOAT=OFF \
	-DUSE_INCLUDED_LIBZIP=OFF \
	-DUSE_INCLUDED_SSL=OFF \
	-DUSE_INCLUDED_ZLIB=OFF \
	-DUSE_PLATFORM_UUID=ON

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
%{_libdir}/lib3mf.so.*.*.*
%ghost %{_libdir}/lib3mf.so.2

%files devel
%defattr(644,root,root,755)
%doc CONTRIBUTING.md
%{_libdir}/lib3mf.so
%{_includedir}/lib3MF
%{_pkgconfigdir}/lib3mf.pc
%{_libdir}/cmake/lib3mf
