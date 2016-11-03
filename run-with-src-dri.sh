#!/bin/bash
source $HOME/src/fdo/menv

export LIBGL_DRIVERS_PATH=$MESA_DIR/lib
export GBM_DRIVERS_PATH=$MESA_DIR/lib

: ${GDB=0}
if [ "$GDB" == "0" ]; then
  GDB=""
else
  GDB="gdb --args"
fi
: ${AUB=0}
if [ "$AUB" == "0" ]; then
  AUB=""
else
  AUB="intel_aubdump"
fi
if [ -z "$PIGLIT_PLATFORM" -a -z "$DISPLAY" ]; then
  export PIGLIT_PLATFORM=gbm
fi
$AUB $GDB $*
