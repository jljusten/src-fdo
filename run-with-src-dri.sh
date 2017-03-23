#!/bin/bash
source $HOME/src/fdo/menv

export LIBGL_DRIVERS_PATH=$MESA_DIR/lib
export GBM_DRIVERS_PATH=$MESA_DIR/lib

: ${GDB=0}
if [ "$GDB" != "0" ]; then
    set - gdb --args "$@"
fi

: ${AUB=0}
if [ "$AUB" != "0" ]; then
    set - intel_aubdump "$@"
fi

: ${SHADER_CACHE=0}
if [ "$SHADER_CACHE" != "0" ]; then
    export INTEL_SHADER_CACHE=1
    export MESA_GLSL_CACHE=1
else
    unset INTEL_SHADER_CACHE
    export MESA_GLSL_CACHE=0
fi

if [ -z "$PIGLIT_PLATFORM" -a -z "$DISPLAY" ]; then
  export PIGLIT_PLATFORM=gbm
fi

exec "$@"
