#!/bin/bash
source $(dirname $0)/menv

export LIBGL_DRIVERS_PATH=$MESA_DIR/lib
export EGL_DRIVERS_PATH=$MESA_DIR/lib
export GBM_DRIVERS_PATH=$MESA_DIR/lib

: ${GDB=0}
if [ "$GDB" != "0" ]; then
    set - gdb --args "$@"
fi

: ${AUB=0}
if [ "$AUB" != "0" ]; then
    set - intel_aubdump "$@"
fi

: ${SHADER_CACHE=1}
if [ "$SHADER_CACHE" != "0" ]; then
    export INTEL_SHADER_CACHE=1
    export MESA_GLSL_CACHE_DISABLE=0
else
    export INTEL_SHADER_CACHE=0
    export MESA_GLSL_CACHE_DISABLE=1
fi

if [ -z "$PIGLIT_PLATFORM" -a -z "$DISPLAY" ]; then
  export PIGLIT_PLATFORM=gbm
fi

exec "$@"
