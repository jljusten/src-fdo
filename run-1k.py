#!/usr/bin/env python3
# Jordan Justen : this file is public domain

import os
import socket
import subprocess
import sys
import tempfile
import time

isexec = lambda fn: os.path.isfile(fn) and os.access(fn, os.X_OK)

here = os.path.dirname(os.path.abspath(sys.argv[0]))

piglit = os.path.join(here, 'piglit')
if not isexec(os.path.join(piglit, 'piglit')):
    piglit = os.path.join(os.path.expanduser('~'), 'src', 'fdo', 'piglit')

bin = os.path.join(piglit, 'piglit')

if not isexec(bin):
    print(bin, 'is not executable')
    sys.exit(1)

os.environ['vblank_mode'] = '0'
os.environ['NIR_VALIDATE'] = '0'
os.environ.pop('DISPLAY', None)

timenow = time.strftime('%y%m%d-%H%M%S')

results_subdir = os.environ.get('RESULTS_SUBDIR', socket.gethostname())

log_dir = os.path.join(here, 'results', results_subdir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log = os.path.join(log_dir, f'1k-{timenow}')

test_list = os.path.join(os.path.expanduser('~'), 'src', 'fdo', 'test-lists',
                         'piglit-gen12-simics.txt')
tests = ['--test-list', test_list, 'all']

cmd_env = os.environ.get('CMD_ENV', os.path.join(here, 'run-with-dev-mesa'))

cmd = [bin, 'run'] + tests + [log] + sys.argv[1:]
print(' '.join(cmd))

full_cmd = [cmd_env] + cmd

os.nice(20)
os.chdir(piglit)
start = time.time()
cp = subprocess.run(args=full_cmd)
elapsed = time.time() - start

print(f'{elapsed:.1f}s elapsed')
sys.exit(cp.returncode)
