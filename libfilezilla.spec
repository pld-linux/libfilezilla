#
# Conditional build:
%bcond_without	apidocs		# doxygen API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# "make check"
#
Summary:	Library for high-performing platform-independent programs
Summary(pl.UTF-8):	Biblioteka do wydajnych programów niezależnych od platformy
Name:		libfilezilla
Version:	0.17.1
Release:	2
License:	GPL v2
Group:		Libraries
Source0:	https://download.filezilla-project.org/libfilezilla/%{name}-%{version}.tar.bz2
# Source0-md5:	7cecda7c08f141223076487490374cb5
URL:		https://lib.filezilla-project.org/
%{?with_tests:BuildRequires:	cppunit-devel >= 1.13.0}
%{?with_apidocs:BuildRequires:	doxygen}
%if %{with tests} && %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.11.0
BuildRequires:	gnutls-devel >= 3.5.7
BuildRequires:	libtool >= 2:2
BuildRequires:	nettle-devel >= 3.1
BuildRequires:	pkgconfig >= 1:0.7
# -std=c++17
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfilezilla is a free, open source C++ library, offering some basic
functionality to build high-performing, platform-independent programs.
Some of the highlights include:

- A typesafe, multi-threaded event system that's very simple to use
  yet extremely efficient
- Timers for periodic events
- A datetime class that not only tracks timestamp but also their
  accuracy, which simplifies dealing with timestamps originating from
  different sources
- Simple process handling for spawning child processes with redirected
  I/O

%description -l pl.UTF-8
libfilezilla to wolnodostępna biblioteka C++ o otwartych źródłach,
oferująca pewną podstawową funkcjonalność do tworzenia wydajnych
programów niezależnych od platformy. Uwzględnione funkcje obejmują:
- bezpieczny pod względem typów, wielowątkowy system zdarzeń -
  bardzo prosty w użyciu, a jednocześnie bardzo wydajny
- zegary do zdarzeń regularnych
- klasa daty i czasu nie tylko śledząca znacznik czasu, ale także jego
  dokładność, co upraszcza obsługę znaczników czasu pochodzących z
  różnych źródeł
- prostą obsługę procesów do tworzenia procesów potomnych z
  przekierowanym wejściem/wyjściem

%package devel
Summary:	Header files for libfilezilla library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libfilezilla
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for libfilezilla library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libfilezilla.

%package static
Summary:	Static libfilezilla library
Summary(pl.UTF-8):	Statyczna biblioteka libfilezilla
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libfilezilla library.

%description static -l pl.UTF-8
Statyczna biblioteka libfilezilla.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q

cd locales
%{__mv} bg{_BG,}.po
%{__mv} ca{_ES,}@valencia.po
%{__mv} cs{_CZ,}.po
%{__mv} fa{_IR,}.po
%{__mv} fi{_FI,}.po
%{__mv} gl{_ES,}.po
%{__mv} he{_IL,}.po
%{__mv} hu{_HU,}.po
%{__mv} id{_ID,}.po
%{__mv} ja{_JP,}.po
%{__mv} ko{_KR,}.po
%{__mv} lo{_LA,}.po
%{__mv} lt{_LT,}.po
%{__mv} lv{_LV,}.po
%{__mv} mk{_MK,}.po
%{__mv} nb{_NO,}.po
%{__mv} nn{_NO,}.po
%{__mv} pl{_PL,}.po
%{__mv} pt{_PT,}.po
%{__mv} ro{_RO,}.po
%{__mv} sk{_SK,}.po
%{__mv} sl{_SI,}.po
%{__mv} th{_TH,}.po
%{__mv} uk{_UA,}.po
%{__mv} vi{_VN,}.po

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
# wide char conversion test fails with plain C locale
LC_ALL=C.UTF-8 \
%{__make} check
%endif

%if %{with apidocs}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# not supported by glibc (as of 2.25)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/co

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libfilezilla.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfilezilla.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfilezilla.so
%{_includedir}/libfilezilla
%{_pkgconfigdir}/libfilezilla.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfilezilla.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/doxygen-doc/html/*
%endif
