%define major 0
%define lib %mklibname %{name} %major
%define devel %mklibname -d %{name}

Name: t4k_common
Version: 0.1.1
Summary: Files used by all Tux4Kids applications/games

Group: System/Libraries
Source0: http://alioth.debian.org/frs/download.php/3540/t4k_common-%{version}.tar.gz
Release: 4
License: LGPLv3
Patch0: t4k_common-0.1.1-braindamage.patch
Patch1: t4k_common-0.1.1-libpng-1.5.patch
Requires: %lib = %{version}-%{release}
BuildRequires: pkgconfig(SDL_Pango)
BuildRequires: pkgconfig(SDL_image)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(sdl) >= 1.2.0
BuildRequires: pkgconfig(SDL_mixer)
BuildRequires: pkgconfig(SDL_net)
BuildRequires: pkgconfig(libpng)
BuildRequires: gettext-devel

%description
Files used by all Tux4Kids applications/games

%package -n %lib
Summary: Libraries used by all Tux4Kids applications/games

Group: System/Libraries

%description -n %lib
Libraries used by all Tux4Kids applications/games

%package -n %devel
Summary: Development files for the Tux4Kids common library

Group: Development/C
Requires: %lib = %{version}-%{release}

%description -n %devel
Development files for the Tux4Kids common library

%prep
%setup
%apply_patches

%build
autoreconf -fi
%configure --disable-static
%make

%install
%makeinstall_std

%files
%{_datadir}/%{name}

%files -n %lib
%{_libdir}/libt4k_common.so.%{major}*

%files -n %devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libt4k_common.so
