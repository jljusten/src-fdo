#!/bin/bash
export MESA_GLES_VERSION_OVERRIDE=3.1
export MESA_EXTENSION_OVERRIDE=GL_ARB_compute_shader
$HOME/src/fdo/run-with-src-dri.sh $*
