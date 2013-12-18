all:
	test -d macros       || git clone git://anongit.freedesktop.org/xorg/util/macros
	test -d xproto       || git clone git://anongit.freedesktop.org/xorg/proto/xproto
	test -d kbproto      || git clone git://anongit.freedesktop.org/xorg/proto/kbproto
	test -d libX11       || git clone git://anongit.freedesktop.org/xorg/lib/libX11
	test -d libxkbcommon || git clone git://people.freedesktop.org/xorg/lib/libxkbcommon.git

