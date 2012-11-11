Summary:	Central Regulatory Domain Agent
Name:		crda
Version:	1.1.2
Release:	2
License:	ISC
Group:		Networking/Daemons
Source0:	http://wireless.kernel.org/download/crda/%{name}-%{version}.tar.bz2
# Source0-md5:	5226f65aebacf94baaf820f8b4e06df4
Patch0:		%{name}-nl3.patch
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel
BuildRequires:	python-M2Crypto
BuildRequires:	wireless-regdb
Requires:	udev
Requires:	wireless-regdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CRDA acts as the udev helper for communication between the kernel and
userspace for regulatory compliance. It relies on nl80211 for
communication. CRDA is intended to be run only through udev
communication from the kernel. The user should never have to run it
manually except if debugging udev issues.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}"
%{__make} \
	CC="%{__cc}"				\
	REG_BIN=%{_datadir}/crda/regulatory.bin	\
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	SBINDIR=%{_sbindir}/	\
	UDEV_RULE_DIR=%{_prefix}/lib/udev/rules.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/crda
%attr(755,root,root) %{_sbindir}/regdbdump
%{_mandir}/man8/*
%{_prefix}/lib/udev/rules.d/85-regulatory.rules

