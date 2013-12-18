DIRS=glproto drm macros dri2proto mesa

all: $(DIRS)

.PHONY: $(DIRS)

glproto:
	cd glproto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install

drm:
	cd drm && \
	  ./autogen.sh --prefix=$(WLD) --enable-nouveau-experimental-api --without-cairo && \
	  make && make install

macros:
	cd macros && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install

dri2proto:
	cd dri2proto && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install

mesa_new:
	cd mesa && \
	  ./autogen.sh --prefix=$(WLD) && \
	  make && make install

mesa:
	cd mesa && \
	  ./autogen.sh --prefix=$(WLD) --enable-gles2 --disable-gallium-egl \
	  --with-egl-platforms=x11,drm --enable-gbm --with-dri-drivers=i965 \
	  --enable-shared-glapi && \
	  make && make install

