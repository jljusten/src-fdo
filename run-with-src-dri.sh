#!/bin/bash
source $HOME/src/fdo/menv
export LIBGL_DRIVERS_PATH=$HOME/src/fdo/mesa/lib
$*
