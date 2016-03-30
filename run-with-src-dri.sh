#!/bin/bash
source $HOME/src/fdo/menv
export LIBGL_DRIVERS_PATH=$HOME/src/fdo/mesa/lib
export GBM_DRIVERS_PATH=$HOME/src/fdo/mesa/lib
: ${GDB=0}
if [ "$GDB" == "0" ]; then
  GDB=""
else
  GDB="gdb --args"
fi
if [ -z "$PIGLIT_PLATFORM" -a -z "$DISPLAY" ]; then
  export PIGLIT_PLATFORM=gbm
fi
$GDB $*
