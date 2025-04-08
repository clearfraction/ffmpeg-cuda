%define cuda_prefix /usr/local-cuda
%define cuda_bindir /usr/local-cuda/bin
%define cuda_includedir /usr/local-cuda/include
%define cuda_libdir /usr/local-cuda/lib64
%define cuda_datadir /usr/local-cuda/share

%global gitdate 20240405
%global commit0 083443d67cb159ce469e5d902346b8d0c2cd1c93
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global shortname0 ffmpeg

Summary:        Digital VCR and streaming server
Name:           ffmpeg-cuda
Version:        7.1
Release:        109
License:        GPLv2+
URL:            http://ffmpeg.org
Source0:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
Requires:       libvdpau-lib
Requires:       %{name}-libs = %{version}-%{release}
#Requires:       %%{name}-filemap = %%{version}-%%{release}
BuildRequires:  gmp-dev
BuildRequires:  bzip2-dev
BuildRequires:  fdk-aac-dev
BuildRequires:  fontconfig-dev
BuildRequires:  freetype-dev
BuildRequires:  gnutls-dev
BuildRequires:  gsm-dev
BuildRequires:  libmp3lame-dev
BuildRequires:  jack2-dev
BuildRequires:  ladspa_sdk-dev
BuildRequires:  libass-dev
BuildRequires:  libgcrypt-devel
BuildRequires:  mesa-dev
BuildRequires:  libmodplug-dev
BuildRequires:  v4l-utils-dev
BuildRequires:  libvorbis-dev
BuildRequires:  libvpx-dev
BuildRequires:  mediasdk-dev
BuildRequires:  libXvMC-dev
BuildRequires:  libva-dev
BuildRequires:  yasm
BuildRequires:  libwebp-dev
BuildRequires:  libjpeg-turbo-dev
BuildRequires:  opus-dev
BuildRequires:  pulseaudio-dev
BuildRequires:  perl-Pod-POM-man
BuildRequires:  SDL2-dev
BuildRequires:  snappy-dev
BuildRequires:  speex-dev
BuildRequires:  subversion
BuildRequires:  texinfo
BuildRequires:  wavpack-dev
BuildRequires:  x264-dev
BuildRequires:  x265-dev
BuildRequires:  zlib-dev
BuildRequires:  libdrm-dev
BuildRequires:  alsa-lib-dev
BuildRequires:  rtmpdump-dev
BuildRequires:  pkgconfig(libmfx)
BuildRequires:  appstream-glib-dev
BuildRequires:  dav1d-dev
BuildRequires:  Vulkan-Loader-dev Vulkan-Loader 
BuildRequires:  Vulkan-Headers-dev Vulkan-Tools Vulkan-Headers
BuildRequires:  glslang-dev glslang
BuildRequires:  SPIRV-Tools-dev SPIRV-Cross-dev
BuildRequires:  SVT-AV1-dev
BuildRequires:  libvdpau-dev
BuildRequires:  libplacebo-dev
BuildRequires:  zimg-dev
BuildRequires:  xvidcore-dev
BuildRequires:  vid.stab-dev
BuildRequires:  libtheora-dev
BuildRequires:  libssh-dev libssh2-dev
BuildRequires:  srt-dev
BuildRequires:  speex-dev
BuildRequires:  librsvg-dev
BuildRequires:  libopenmpt-dev
BuildRequires:  openjpeg-dev
BuildRequires:  libaom-dev
BuildRequires:  ladspa_sdk-dev
#BuildRequires:  nv-codec-headers nv-codec-headers-dev



%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}
Recommends:	fdk-aac

%description    libs
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package        dev
Summary:        Development package for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires:       pkg-config

%description    dev
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

%prep
%setup -n ffmpeg-%{version}
# erase glslang flags from configure checks
sed -i "s|-lOSDependent||" configure
sed -i "s|-lOGLCompiler||" configure
sed -i "s|-lMachineIndependent||" configure
sed -i "s|-lGenericCodeGen||" configure
# newest nv-codev-headers
unset https_proxy
git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
pushd nv-codec-headers
    make
    make PREFIX=/usr LIBDIR=lib64 install
popd

%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export PKG_CONFIG_PATH="/usr/local/lib64/pkgconfig"
export LDFLAGS="-Wl,-rpath=/usr/local-cuda/lib64,-rpath=/opt/3rd-party/bundles/clearfraction/usr/local-cuda/lib64,-rpath=/opt/3rd-party/bundles/clearfraction/usr/lib64 "
export CFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export FCFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export FFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export CXXFLAGS="$CXXFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
./configure --disable-static --extra-ldflags='-ldl' \
    --prefix=%{cuda_prefix} \
    --bindir=%{cuda_bindir} \
    --datadir=%{cuda_datadir}/%{shortname0} \
    --incdir=%{cuda_includedir}/%{shortname0} \
    --libdir=%{cuda_libdir} \
    --shlibdir=%{cuda_libdir} \
    --enable-pixelutils \
    --extra-ldflags='-ldl' \
    --enable-vaapi \
    --enable-bzlib \
    --enable-libdrm \
    --enable-fontconfig \
    --enable-gcrypt \
    --enable-gmp --enable-version3 \
    --enable-gnutls \
    --enable-ladspa \
    --enable-libass \
    --enable-libjack \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgsm \
    --enable-libmp3lame \
    --enable-opengl \
    --enable-libopus \
    --enable-libpulse \
    --enable-libsnappy \
    --enable-libspeex \
    --enable-libvorbis \
    --enable-libv4l2 \
    --enable-sdl2 \
    --enable-libvpx \
    --enable-libwebp \
    --enable-libx264 \
    --enable-libx265 \
    --enable-avfilter \
    --enable-swscale \
    --enable-postproc \
    --enable-pthreads \
    --enable-librtmp \
    --enable-libmfx \
    --disable-static \
    --enable-shared \
    --enable-gpl \
    --disable-debug \
    --disable-doc \
    --enable-libfdk-aac --enable-nonfree \
    --enable-libdav1d \
    --enable-libsvtav1 \
    --enable-nvdec --enable-nvenc --enable-vdpau \
    --enable-ladspa \
    --enable-libaom \
    --enable-libopenjpeg \
    --enable-libopenmpt \
    --enable-librsvg \
    --enable-libspeex \
    --enable-libsrt \
    --enable-libssh \
    --enable-libtheora \
    --enable-libvidstab \
    --enable-libxcb \
    --enable-libzimg \
    --enable-libplacebo \
    --enable-vulkan \
    --enable-libglslang

make  %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
rm -rf %{buildroot}%{cuda_datadir}/examples
mv %{buildroot}%{cuda_prefix} %{buildroot}/usr/local
pushd %{buildroot}/usr
ln -s local local-cuda
popd


%post libs -p /usr/bin/ldconfig

%postun libs -p /usr/bin/ldconfig

%files
%defattr(-,root,root,-)
/usr/local/bin/ffmpeg
/usr/local/bin/ffplay
/usr/local/bin/ffprobe
/usr/local/share/%{shortname0}

%files libs
%defattr(-,root,root,-)
/usr/local/lib64/lib*.so.*
/usr/local-cuda

%files dev
%defattr(-,root,root,-)
/usr/local/include/%{shortname0}
/usr/local/lib64/pkgconfig/lib*.pc
/usr/local/lib64/lib*.so


# based on https://github.com/UnitedRPMs/ffmpeg
# and https://github.com/clearlinux-pkgs/not-ffmpeg
