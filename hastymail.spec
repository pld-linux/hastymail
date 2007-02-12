# TODO
# - use webapps
Summary:	Hastymail - easy-to-use, fast webmail system
Summary(pl.UTF-8):   Hastymail - łatwy w użyciu, szybki system webmail
Name:		hastymail
Version:	1.5
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/hastymail/%{name}-%{version}.tar.bz2
# Source0-md5:	bbff61a6986356ec235cf2310a08d811
Source1:	%{name}.htaccess
URL:		http://hastymail.sourceforge.net/
Requires(post):	fileutils
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires:	php(gettext)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webserver
Requires:	webserver(php)
Provides:	webmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_hastymaildir	/home/services/httpd/html/%{name}
%define		vardir		/var/lib/%{name}

%description
Hastymail is yet another webmail IMAP client written in PHP. It's
designed for speed, RFC compatibility and security. Hastymail is
intended to be the fastest PHP IMAP client around.

%description -l pl.UTF-8
Hastymail to jeszcze jeden webmailowy klient IMAP napisany w PHP.
Został zaprojektowany z myślą o szybkości, kompatybilności z RFC i
bezpieczeństwie. Hastymail ma być najszybszym istniejącym klientem
IMAP w PHP.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_hastymaildir},%{_sysconfdir}/httpd/httpd.conf} \
	$RPM_BUILD_ROOT%{vardir}/{settings/attachments,include}

cp -a {filter,html,idna,images,index.php,lang,lib,templates,themes} $RPM_BUILD_ROOT%{_hastymaildir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_hastymaildir}/.htaccess
sed -e "s@/var/hastymail@%{vardir}@" hastymail.conf-example > \
	$RPM_BUILD_ROOT%{_sysconfdir}/hastymail.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 0 ]; then
	SECRET=`dd if=/dev/urandom bs=1 count=42 2>/dev/null | od -a -w42 | cut -c8- | sed -e 's![^[:alnum:]]!!g' | xargs`
	if [ -n "$SECRET" ] ; then
		echo "Updating authentication secret in config files..."
		sed -i -e 's#\"KEY\"#\"$SECRET\"#g' %{_hastymaildir}/.htaccess
	else
		echo "Remember to update secret in "
		echo "    %{_hastymaildir}/.htaccess"
	fi
fi
%service -q httpd restart

%files
%defattr(644,root,root,755)
%doc INSTALL CHANGES TODO README DEVELOPMENT RELEASE.NOTES hastymail.conf-example
%dir %{_hastymaildir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%dir %{vardir}
%dir %attr(700,http,http) %{vardir}/settings
%dir %attr(700,http,http) %{vardir}/settings/attachments
%{_hastymaildir}/filter
%{_hastymaildir}/html
%{_hastymaildir}/idna
%{_hastymaildir}/images
%{_hastymaildir}/index.php
%{_hastymaildir}/lang
%{_hastymaildir}/lib
%{_hastymaildir}/templates
%{_hastymaildir}/themes
%config(noreplace) %verify(not md5 mtime size) %{_hastymaildir}/.htaccess
