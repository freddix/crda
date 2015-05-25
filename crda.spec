Summary:	Central Regulatory Domain Agent
Name:		crda
Version:	3.18
Release:	1
License:	ISC
Group:		Networking/Daemons
Source0:	https://kernel.org/pub/software/network/crda/%{name}-%{version}.tar.xz
# Source0-md5:	0431fef3067bf503dfb464069f06163a
Patch0:		%{name}-regdb.patch
Patch1:		0001-crda-Fix-the-linking-order-to-avoid-compilation-erro.patch
Patch2:		0002-crda-Add-DESTDIR-support-in-install-libreg-rules-in-.patch
Patch3:		0001-Makefile-Link-libreg.so-against-the-crypto-library.patch
Patch4:		0001-Makefile-Don-t-run-ldconfig.patch
URL:		http://wireless.kernel.org/en/developers/Regulatory/CRDA
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel
BuildRequires:	pkg-config
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
	LIBDIR=%{_libdir}/	\
	SBINDIR=%{_sbindir}/	\
	UDEV_RULE_DIR=%{_prefix}/lib/udev/rules.d/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/crda
%attr(755,root,root) %{_sbindir}/regdbdump
%attr(755,root,root) %{_libdir}/libreg.so
%{_mandir}/man8/*
%{_prefix}/lib/udev/rules.d/85-regulatory.rules

