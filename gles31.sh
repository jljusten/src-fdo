#!/usr/bin/env bash
# Jordan Justen : this file is public domain

export MESA_GLES_VERSION_OVERRIDE=3.1
export MESA_EXTENSION_OVERRIDE=GL_ARB_compute_shader
$HOME/src/fdo/run-with-src-dri.sh $*
