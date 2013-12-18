all:
	test -d drm       || git clone git://anongit.freedesktop.org/git/mesa/drm
	test -d macros    || git clone git://anongit.freedesktop.org/git/xorg/util/macros
	test -d glproto   || git clone git://anongit.freedesktop.org/xorg/proto/glproto
	test -d dri2proto || git clone git://anongit.freedesktop.org/xorg/proto/dri2proto
	test -d mesa      || git clone git://anongit.freedesktop.org/mesa/mesa

