all:
	cd macros && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd xproto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd kbproto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd libX11 && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd libxkbcommon && \
	  ./autogen.sh --prefix=$(WLD) \
	    --with-xkb-config-root=/usr/share/X11/xkb && \
	  make && make install

