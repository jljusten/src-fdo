#!/usr/bin/env bash
#export PIGLIT_PLATFORM=gbm
export MESA_GL_VERSION_OVERRIDE=4.3
export MESA_GLSL_VERSION_OVERRIDE=430
export MESA_EXTENSION_OVERRIDE=GL_ARB_compute_shader
$HOME/src/fdo/run-with-src-dri.sh $*
