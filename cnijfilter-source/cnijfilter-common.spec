%define VERSION 3.30
%define RELEASE 1

%define _prefix	/usr/local
%define _bindir %{_prefix}/bin
%define _libdir /usr/lib
%define _ppddir /usr

%define PR1	ip2700
%define PR2	mx340
%define PR3	mx350
%define PR4	mx870
%define BUILD_PR 	%{PR1} %{PR2} %{PR3} %{PR4}

%define PKG1 	ip2700series
%define PKG2 	mx340series
%define PKG3 	mx350series
%define PKG4 	mx870series

%define PR1_ID 	364
%define PR2_ID 	365
%define PR3_ID 	366
%define PR4_ID 	367
%define BUILD_PR_ID 	%{PR1_ID} %{PR2_ID} %{PR3_ID} %{PR4_ID}

%define CNBP_LIBS libcnbpcmcm libcnbpcnclapi libcnbpcnclbjcmd libcnbpcnclui libcnbpess libcnbpo
%define COM_LIBS libcnnet

Summary: IJ Printer Driver Ver.%{VERSION} for Linux
Name: cnijfilter-common
Version: %{VERSION}
Release: %{RELEASE}
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Source0: cnijfilter-source-%{version}-%{release}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
Requires:  cups popt
#BuildRequires: gtk-devel cups-devel 

# PR1 PKG1 PR1_ID
%package -n cnijfilter-%{PKG1}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

# PR2 PKG2 PR2_ID
%package -n cnijfilter-%{PKG2}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

# PR3 PKG3 PR3_ID
%package -n cnijfilter-%{PKG3}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

# PR4 PKG4 PR4_ID
%package -n cnijfilter-%{PKG4}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng


%description
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

# PR1 PKG1 PR1_ID
%description -n cnijfilter-%{PKG1}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

# PR1 PKG2 PR2_ID
%description -n cnijfilter-%{PKG2}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

# PR3 PKG3 PR3_ID
%description -n cnijfilter-%{PKG3}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

# PR4 PKG4 PR4_ID
%description -n cnijfilter-%{PKG4}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.


%prep
%setup -q -n  cnijfilter-source-%{version}-%{RELEASE}

cd libs
    ./autogen.sh --prefix=%{_prefix} 

cd ../cngpij
    ./autogen.sh --prefix=%{_prefix} --enable-progpath=%{_bindir}

cd ../pstocanonij
    ./autogen.sh --prefix=/usr --enable-progpath=%{_bindir} 

cd ../backend
    ./autogen.sh --prefix=/usr

cd ../backendnet
    ./autogen.sh --prefix=%{_prefix} --enable-progpath=%{_bindir}

cd ../cngpijmon/cnijnpr
    ./autogen.sh --prefix=%{_prefix}

%build
#make 


%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/cups/filter
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/cups/model


# make and install files for printer packages
for PR in %{BUILD_PR}
do
cd  ppd
    ./autogen.sh --prefix=/usr --program-suffix=${PR}
	make clean
	make
	make install DESTDIR=${RPM_BUILD_ROOT}

cd ../cnijfilter
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR} --enable-libpath=%{_libdir}/bjlib --enable-binpath=%{_bindir}
    make clean
    make
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../printui
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR} --datadir=%{_prefix}/share
    make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../lgmon
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR} --enable-progpath=%{_bindir}
    make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../cngpijmon
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR}  --enable-progpath=%{_bindir} --datadir=%{_prefix}/share
	make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ..
done

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/bjlib

install -c -m 644 com/ini/cnnet.ini  		${RPM_BUILD_ROOT}%{_libdir}/bjlib

for PR_ID in %{BUILD_PR_ID}
do
#   install -c -s -m 755 ${PR_ID}/database/*  		${RPM_BUILD_ROOT}%{_libdir}/bjlib
    install -c -m 644 ${PR_ID}/database/*  		${RPM_BUILD_ROOT}%{_libdir}/bjlib
    install -c -s -m 755 ${PR_ID}/libs_bin/*.so.* 	${RPM_BUILD_ROOT}%{_libdir}
done

cd ${RPM_BUILD_ROOT}%{_libdir}
#for PR_ID in %{BUILD_PR_ID}
#do
#	ln -s libcnbpcmcm${PR_ID}.so.* 		libcnbpcmcm${PR_ID}.so
#	ln -s libcnbpcnclapi${PR_ID}.so.*	libcnbpcnclapi${PR_ID}.so
#	ln -s libcnbpcnclbjcmd${PR_ID}.so.* libcnbpcnclbjcmd${PR_ID}.so
#	ln -s libcnbpcnclui${PR_ID}.so.* 	libcnbpcnclui${PR_ID}.so
#	ln -s libcnbpess${PR_ID}.so.* 		libcnbpess${PR_ID}.so
#	ln -s libcnbpo${PR_ID}.so.* 		libcnbpo${PR_ID}.so
#done
cd -

# make and install files for common package
make install DESTDIR=${RPM_BUILD_ROOT}
install -c -s -m 755 com/libs_bin/*.so.* 	${RPM_BUILD_ROOT}%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun
for LIBS in %{COM_LIBS}
do
	if [ -h %{_libdir}/${LIBS}.so ]; then
		rm -f %{_libdir}/${LIBS}.so
	fi	
done
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
fi
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi

# PR1 PKG1 PR1_ID
%post -n cnijfilter-%{PKG1}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG1}
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR1_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR1_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR1}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR1}
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi

# PR2 PKG2 PR2_ID
%post -n cnijfilter-%{PKG2}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG2}
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR2_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR2_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR2}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR2}
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi

# PR3 PKG3 PR3_ID
%post -n cnijfilter-%{PKG3}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG3}
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR3_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR3_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR3}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR3}
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi

# PR4 PKG4 PR4_ID
%post -n cnijfilter-%{PKG4}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG4}
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR4_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR4_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR4}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR4}
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi


%files
%defattr(-,root,root)
%{_libdir}/cups/filter/pstocanonij
%{_libdir}/cups/backend/cnijusb
%{_libdir}/cups/backend/cnijnet
%{_bindir}/cngpij
%{_bindir}/cnijnpr
%{_bindir}/cnijnetprn
%{_libdir}/libcnnet.so*
%attr(644, lp, lp) %{_libdir}/bjlib/cnnet.ini

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


# PR1 PKG1 PR1_ID
%files -n cnijfilter-%{PKG1}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR1}
%{_bindir}/lgmon%{PR1}
%{_bindir}/printui%{PR1}
%{_ppddir}/share/cups/model/canon%{PR1}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR1}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR1}.mo
%{_prefix}/share/cngpijmon%{PR1}/*
%{_prefix}/share/printui%{PR1}/*

%{_bindir}/cif%{PR1}
%{_libdir}/libcnbp*%{PR1_ID}.so*
%{_libdir}/bjlib/cif%{PR1}.conf
%{_libdir}/bjlib/cnb_%{PR1_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR1_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt

# PR2 PKG2 PR2_ID
%files -n cnijfilter-%{PKG2}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR2}
%{_bindir}/lgmon%{PR2}
%{_bindir}/printui%{PR2}
%{_ppddir}/share/cups/model/canon%{PR2}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR2}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR2}.mo
%{_prefix}/share/cngpijmon%{PR2}/*
%{_prefix}/share/printui%{PR2}/*

%{_bindir}/cif%{PR2}
%{_libdir}/libcnbp*%{PR2_ID}.so*
%{_libdir}/bjlib/cif%{PR2}.conf
%{_libdir}/bjlib/cnb_%{PR2_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR2_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt

# PR3 PKG3 PR3_ID
%files -n cnijfilter-%{PKG3}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR3}
%{_bindir}/lgmon%{PR3}
%{_bindir}/printui%{PR3}
%{_ppddir}/share/cups/model/canon%{PR3}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR3}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR3}.mo
%{_prefix}/share/cngpijmon%{PR3}/*
%{_prefix}/share/printui%{PR3}/*

%{_bindir}/cif%{PR3}
%{_libdir}/libcnbp*%{PR3_ID}.so*
%{_libdir}/bjlib/cif%{PR3}.conf
%{_libdir}/bjlib/cnb_%{PR3_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR3_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt

# PR4 PKG4 PR4_ID
%files -n cnijfilter-%{PKG4}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR4}
%{_bindir}/lgmon%{PR4}
%{_bindir}/printui%{PR4}
%{_ppddir}/share/cups/model/canon%{PR4}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR4}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR4}.mo
%{_prefix}/share/cngpijmon%{PR4}/*
%{_prefix}/share/printui%{PR4}/*

%{_bindir}/cif%{PR4}
%{_libdir}/libcnbp*%{PR4_ID}.so*
%{_libdir}/bjlib/cif%{PR4}.conf
%{_libdir}/bjlib/cnb_%{PR4_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR4_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt

%ChangeLog
