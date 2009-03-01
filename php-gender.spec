%define modname gender
%define soname %{modname}.so
%define inifile A89_%{modname}.ini

Summary:	Gender Extension
Name:		php-%{modname}
Version:	0.6.1
Release:	%mkrel 3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/gender/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		gender-0.6.1-typo_fix.diff
Requires:	php-bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gender PHP extension is a port of the gender.c program originally written by
Joerg Michael. The main purpose is to find out the gender of first names. The
actual database contains >40000 first names from 54 countries.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

bunzip2 data/nam_dict.txt.bz2

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -p -i -e "s|/lib\b|/%{_lib}|g" *.m4

perl -pi -e "s|/home/user/|%{_datadir}/%{name}/|g" README

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_datadir}/%{name}

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 data/nam_dict.txt %{buildroot}%{_datadir}/%{name}/
bzip2 -9 %{buildroot}%{_datadir}/%{name}/nam_dict.txt

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS LICENSE README tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
%dir %{_datadir}/%{name}
%attr(0644,root,root) %{_datadir}/%{name}/nam_dict.txt.bz2

