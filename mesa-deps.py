# Jordan Justen : this file is public domain

dirs = ('glproto', 'drm', 'macros', 'dri2proto', 'mesa')

modules = hash(

print modules

'''
all:
	cd glproto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd drm && \
	  ./autogen.sh --prefix=$(WLD) --enable-nouveau-experimental-api && \
	  make && make install
	cd macros && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd dri2proto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install
	cd mesa && \
	  ./autogen.sh --prefix=$(WLD) --enable-gles2 --disable-gallium-egl \
	  --with-egl-platforms=x11,wayland,drm --enable-gbm \
	  --enable-shared-glapi && \
	  make && make install
'''
