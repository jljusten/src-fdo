# Jordan Justen : this file is public domain

all:
	cd pixman && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd cairo && \
	  ./autogen.sh --prefix=$(WLD) \
	    --enable-gl --enable-xcb && \
	  make && make install

