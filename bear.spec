Summary:	Tool that generates a compilation database for clang tooling
Name:		bear
Version:	3.1.1
Release:	1
License:	GPL v3+
Group:		Development/Building
Source0:	https://github.com/rizsotto/Bear/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1eccc34705eac635aa7408c6c01aef86
URL:		https://github.com/rizsotto/Bear
BuildRequires:	cmake >= 3.13
BuildRequires:	gmock-devel >= 1.10
BuildRequires:	grpc-devel >= 1.26
BuildRequires:	gtest-devel >= 1.10
BuildRequires:	libfmt-devel >= 6.1
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	nlohmann-json-devel >= 3.7.3
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 3.11
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	spdlog-devel >= 1.5.0
Requires:	grpc >= 1.26
Requires:	libfmt >= 6.1
Requires:	protobuf-libs >= 3.11
Requires:	spdlog >= 1.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The JSON compilation database is used in the clang project to provide
information on how a single compilation unit is processed. With this,
it is easy to re-run the compilation with alternate programs.

Some build systems natively support generation of JSON compilation
database. For projects which do not use such build tool, Bear
generates the JSON file during build process.

%prep
%setup -q -n Bear-%{version}

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export CPPFLAGS="%{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
%cmake -B build \
	-DCMAKE_INSTALL_BINDIR=%(realpath -m "--relative-to=%{_prefix}" "%{_bindir}") \
	-DCMAKE_INSTALL_LIBDIR=%(realpath -m "--relative-to=%{_prefix}" "%{_libdir}")

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md README.md
%attr(755,root,root) %{_bindir}/bear
%dir %{_libdir}/bear
%attr(755,root,root) %{_libdir}/bear/libexec.so
%attr(755,root,root) %{_libdir}/bear/wrapper
%dir %{_libdir}/bear/wrapper.d
%attr(755,root,root) %{_libdir}/bear/wrapper.d/*
%{_mandir}/man1/bear.1*
%{_mandir}/man1/bear-citnames.1*
%{_mandir}/man1/bear-intercept.1*
