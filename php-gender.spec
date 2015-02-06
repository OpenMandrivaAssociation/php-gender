%define modname gender
%define soname %{modname}.so
%define inifile A89_%{modname}.ini

Summary:	Gender Extension
Name:		php-%{modname}
Version:	1.0.0
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/gender/
Source0:	http://pecl.php.net/get/gender-%{version}.tgz
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
%doc package*.xml CREDITS LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
%dir %{_datadir}/%{name}
%attr(0644,root,root) %{_datadir}/%{name}/nam_dict.txt.bz2



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-15mdv2012.0
+ Revision: 795440
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-14
+ Revision: 761231
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-13
+ Revision: 696423
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-12
+ Revision: 695397
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-11
+ Revision: 646638
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-10mdv2011.0
+ Revision: 629797
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-9mdv2011.0
+ Revision: 628103
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-8mdv2011.0
+ Revision: 600488
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-7mdv2011.0
+ Revision: 588800
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-6mdv2010.1
+ Revision: 514547
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-5mdv2010.1
+ Revision: 485361
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-4mdv2010.1
+ Revision: 468167
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-3mdv2010.0
+ Revision: 451272
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.7.0-2mdv2010.0
+ Revision: 397528
- Rebuild

* Sat Jul 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-1mdv2010.0
+ Revision: 392350
- 0.7.0

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-4mdv2010.0
+ Revision: 376992
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-3mdv2009.1
+ Revision: 346429
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-2mdv2009.1
+ Revision: 341738
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2009.1
+ Revision: 324501
- import php-gender


* Sun Jan 04 2009 Oden Eriksson <oden.eriksson@envitory.se> 0.6.1-1mdv2009.1
- initial Mandriva package


