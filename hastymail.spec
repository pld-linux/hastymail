Summary:	Hastymail - easy-to-use, fast webmail system
Summary(pl):	Hastymail - ³atwy w u¿yciu, szybki system webmail
Name:		hastymail
Version:	0.8
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/hastymail/%{name}-%{version}.tar.bz2
# Source0-md5:	e6b6a36e7f4e1c4731616d2b4d0b0e0e
Source1:	hastymail.htaccess
URL:		http://hastymail.sourceforge.net/
Requires(post):	coreutils
Requires(post):	perl-base
Requires(post):	sed
Requires:	php
Requires:	php-gettext
Requires:	php-pcre
Requires:	webserver
Provides:	webmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_hastymaildir	/home/services/httpd/html/%{name}
%define		vardir		/var/lib/%{name}

%description
Hastymail is yet another webmail IMAP client written in PHP. It's
designed for speed, RFC compatibility and security. Hastymail is
intended to be the fastest PHP IMAP client around.

%description -l pl
Hastymail to jeszcze jeden webmailowy klient IMAP napisany w PHP.
Zosta³ zaprojektowany z my¶l± o szybko¶ci, kompatybilno¶ci z RFC i
bezpieczeñstwie. Hastymail ma byæ najszybszym istniej±cym klientem
IMAP w PHP.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_hastymaildir},%{_sysconfdir}/httpd/httpd.conf} \
	$RPM_BUILD_ROOT%{vardir}/{settings/attachments,include}

cp -a {filter,html,images,index.php,lang,lib,themes} $RPM_BUILD_ROOT%{_hastymaildir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_hastymaildir}/.htaccess
sed -e "s@/var/hastymail@%{vardir}@" hastymail.conf-example > \
	$RPM_BUILD_ROOT%{_sysconfdir}/hastymail.conf

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%doc CHANGES TODO README DEVELOPMENT RELEASE.NOTES  hastymail.conf-example
%dir %{_hastymaildir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%dir %attr(700,http,http) %{vardir}/settings
%dir %attr(700,http,http) %{vardir}/settings/attachments
%{_hastymaildir}/filter
%{_hastymaildir}/html
%{_hastymaildir}/images
%{_hastymaildir}/index.php
%{_hastymaildir}/lang
%{_hastymaildir}/lib
%{_hastymaildir}/themes
%config(noreplace) %verify(not size mtime md5) %{_hastymaildir}/.htaccess
