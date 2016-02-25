#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	re2
Summary:	Ruby bindings to re2
Name:		ruby-%{pkgname}
Version:	0.7.0
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	bc012bbef488bf365022e9cbbcb1ad3f
URL:		http://github.com/mudge/re2
BuildRequires:	re2-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-devel
%if %{with tests}
BuildRequires:	ruby-minitest < 6
BuildRequires:	ruby-minitest >= 5.4
BuildRequires:	ruby-rake-compiler < 1
BuildRequires:	ruby-rake-compiler >= 0.9
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby bindings to re2, an efficient, principled regular expression
library.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

cd ext/%{pkgname}
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}
install -p ext/re2/re2.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{ruby_vendorlibdir}/re2.rb
%{ruby_vendorlibdir}/re2
%{ruby_vendorarchdir}/re2.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
