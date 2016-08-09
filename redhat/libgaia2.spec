%{!?python_site: %define python_site %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')}

Summary: General library to work with points in a semimetric space
Name: libgaia2
Version: 2.4.3
Release: 1
License: Proprietary
Group: System Environment/Libraries
Source: %{name}-%{version}.tar
#Patch0: %{name}-%{version}.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://essentia.upf.edu
BuildRequires: qt-devel
BuildRequires: python-devel
BuildRequires: gcc-c++
BuildRequires: libyaml-devel
BuildRequires: swig
Requires: qt, redhat-lsb

%description
Gaia is a general library that allows you to work with points in a semimetric
space. The points have any number of attributes, each one having a name and a
type, which can be either one of those three: real number, string,
enumeration. In simple words, Gaia allows you to define the following:
  * a structure for your space, which will be determined by the PointLayout.
    Each point has exactly one PointLayout, and as such, points which share the
    same layout are said to be in the same space. A PointLayout actually
    contains a list of dimensions (real or string) which contains attributes of
    each point, as well as their associated names and a tree structure to
    organize them (which you can forget about if you don't care for a specific
    reason)
  * a DataSet, which is basically a collection of Points. All Points in a
    DataSet share the same layout.
  * Transformations, which allow you to take Points in a DataSet (or the whole
    DataSet) and apply them a transformation that returns a new Point (or
    DataSet) in a possibly different output space (eg: with a different
    PointLayout)
  * distance functions, which return the distance between two points in a
    specific space

%prep
%setup -q
#%patch -p1

%build
./waf configure --with-python-bindings --nocache --prefix=/usr/ --with-cyclops
./waf

%install
rm -rf %{buildroot}
./waf install --destdir=%{buildroot}
# copy redhat-specific init scripts
cp packaging/centos5/init.d/cyclopsmaster %{buildroot}/etc/init.d/
cp packaging/centos5/init.d/cyclopsslaves %{buildroot}/etc/init.d/
mv $(readlink -m %{buildroot}%{python_site}/../dist-packages) %{buildroot}%{python_site}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
/usr/lib/libgaia2.a
/usr/lib/pkgconfig/gaia2.pc

# python
%package python
Summary: Gaia2 Python Bindings
Group: System Environment/Libraries
Requires: libgaia2 = %{version}-%{release}

%description python
Python bindings for libgaia2

%files python
%defattr(-, root, root, 0755)
%{python_site}/*


# tools
%package tools
Summary: Gaia2 Utilities
Group: System Environment/Libraries
Requires: libgaia2 = %{version}-%{release}

%description tools
Utilities for libgaia2

%files tools
%defattr(-, root, root, 0755)
/usr/bin/gaiainfo
/usr/bin/gaiamerge
/usr/bin/gaia22to23fl
/usr/bin/gaiafusion
/usr/bin/gaiafreeze
/usr/bin/gaiabench

# tools
%package cyclops
Summary: Gaia2 Cyclops
Group: System Environment/Libraries
Requires: libgaia2 = %{version}-%{release}
Requires: cronolog
Requires: python-yaml

%description cyclops
Cyclops for libgaia2


%files cyclops
%defattr(-, root, root, 0755)
/usr/bin/cyclops
/usr/bin/cyclopsmaster
%config(noreplace) /etc/cyclops/master.yaml
/etc/init.d/cyclopsmaster
/etc/init.d/cyclopsslaves

%pre cyclops
/usr/sbin/useradd -c "Cyclops" -K UID_MAX=499 \
	-s /bin/false -r -d /var/run/cyclops -m cyclops 2>/dev/null || :

%post cyclops
/sbin/chkconfig --add cyclopsmaster
/sbin/chkconfig --add cyclopsslaves

%preun cyclops
if [ $1 = 0 ]; then
   /usr/sbin/userdel cyclops 2>/dev/null || :
   /usr/sbin/groupdel cyclops 2>/dev/null || :
   /sbin/chkconfig --del cyclopsmaster
   /sbin/chkconfig --del cyclopsslaves
fi
exit 0

%postun cyclops
if [ "$1" -ge 1 ]; then
	/etc/rc.d/init.d/cyclopsmaster stop >/dev/null 2>&1 || :
fi


# devel
%package devel
Summary: Gaia2 Utilities
Group: System Environment/Libraries
Requires: libgaia2 = %{version}-%{release}

%description devel
Header files for libgaia2

%files devel
%defattr(-, root, root, 0755)
/usr/include/*



%changelog
