Summary:	Fast Webmail
Name:		hastymail
Version:	0.7
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/hastymail/hastymail-%{version}.tar.bz2
# Source0-md5:	5b62aa07029da910aa9b9eebae2320e4
Source1:	hastymail.htaccess
Requires:	php
Requires:	php-gettext
Requires:	php-pcre
Requires:	webserver
Requires(pre):	sed
Provides:	webmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_hastymaildir	/home/services/httpd/html/%{name}

%description
HastyMail is an easy-to-use, fast webmail system

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_hastymaildir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf
install -d $RPM_BUILD_ROOT/var/%{name}/settings/attachments
install -d $RPM_BUILD_ROOT/var/%{name}/include

cp -a {filter,html,images,index.php,lang,lib,themes} $RPM_BUILD_ROOT%{_hastymaildir}

cp hastymail.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/hastymail.conf
cp %{SOURCE1} $RPM_BUILD_ROOT%{_hastymaildir}/.htaccess


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES TODO README DEVELOPMENT RELEASE.NOTES  hastymail.conf-example
%dir %{_hastymaildir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%dir %attr(700,http,http) /var/%{name}/settings
%dir %attr(700,http,http) /var/%{name}/settings/attachments
%{_hastymaildir}/filter
%{_hastymaildir}/html
%{_hastymaildir}/images
%{_hastymaildir}/index.php
%{_hastymaildir}/lang
%{_hastymaildir}/lib
%{_hastymaildir}/themes
%config(noreplace) %{_hastymaildir}/.htaccess

%post
SECRET=`dd if=/dev/random bs=10b count=1 | od -a | sed -e 's![^[:alnum:]]!!g'`
if [ -n "$SECRET" ] ; then
	echo "Updating authentication secret in config files..."
	perl -pi -e "s/KEY/$SECRET/" %{_hastymaildir}/.htaccess
else
	echo "Remember to update secret in "
	echo "    %{_hastymaildir}/.htaccess"
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi
