%define name	t4k_common
%define version	0.0.3
%define release	1

%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

Name:           %{name}
Version:        %{version}
Release:        %mkrel %{release}
Summary:        Tux4Kids common files
Group:          Games/Other
License:        GPLv3+
URL:            http://tux4kids.alioth.debian.org
# have to change with each new release as the number after download.php changes :(
Source0:        http://alioth.debian.org/frs/download.php/3439/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_Pango-devel
BuildRequires:	SDL_net-devel
BuildRequires:	librsvg2-devel
BuildRequires:  libxml2-devel
BuildRequires:	cairo-devel
BuildRequires:	png-devel

%description
Files shared by tuxmath, tuxtype, and possibly other Tux4Kids
apps in the future.

%package -n %{libname}
Summary:        Library of code shared between Tux4Kids apps
Group:          System/Libraries

%description -n %{libname}
Library of code shared by tuxmath, tuxtype, and possibly other tux4kids
apps in the future.

%package -n %{devname}
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains libraries and header files for developing applications
that use %{libname}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--disable-doxygen-doc
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# we don't want these
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%doc README ChangeLog
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
