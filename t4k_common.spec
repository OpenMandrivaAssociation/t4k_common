%define major 0
%define lib %mklibname %{name} %major
%define devel %mklibname -d %{name}

Name: t4k_common
Version: 0.1.1
Summary: Files used by all Tux4Kids applications/games

Group: System/Libraries
Source0: http://alioth.debian.org/frs/download.php/3540/t4k_common-%{version}.tar.gz
Release: 5
License: LGPLv3
Patch0: t4k_common-0.1.1-braindamage.patch
Patch1: t4k_common-0.1.1-libpng-1.5.patch
Requires: %lib = %{version}-%{release}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
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
%autopatch -p1
# The bundled header hides u8_mbtouc_unsafe unless this gnulib
# module macro is set. linebreak.c calls it either way.
sed -i 's/#ifdef GNULIB_UNISTR_U8_MBTOUC_UNSAFE/#if 1/' src/linebreak/unistr.h
# C23 made true and false keywords, so the local enum is illegal.
sed -i '/^#ifndef bool$/,/^#endif$/c #include <stdbool.h>' src/t4k_common.h
# An empty parameter list is (void) in C23. The definition takes a bool.
sed -i 's/set_font_size();/set_font_size(bool uniform);/' src/t4k_menu.c
# node->children is an xmlNode, not an xmlAttr.
sed -i 's/xmlAttr \*current, \*child;/xmlAttr *current; xmlNode *child;/' src/t4k_menu.c

%build
# Pointer types in the menu callbacks do not match. Keep those as warnings.
export CFLAGS="%{optflags} -Wno-error=incompatible-pointer-types -Wno-error=incompatible-function-pointer-types -Wno-error=int-conversion"
autoreconf -fi
%configure --disable-static
# Generated libtool is a no-op after slibtoolize. Link with slibtool.
%make LIBTOOL=slibtool-shared

%install
%makeinstall_std LIBTOOL=slibtool-shared

%files
%{_datadir}/%{name}

%files -n %lib
%{_libdir}/libt4k_common.so.%{major}*

%files -n %devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libt4k_common.so
