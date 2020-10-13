#!/usr/bin/env bash
source $HOME/src/fdo/menv
#export MESA_EXTENSION_OVERRIDE="GL_ARB_geometry_shader4 GL_ARB_texture_multisample"
export LIBGL_DRIVERS_PATH=$MESA_DIR/lib
export MESA_GL_VERSION_OVERRIDE=3.2
export MESA_GLSL_VERSION_OVERRIDE=150
$*
