#!/usr/bin/env python3
# Jordan Justen : this file is public domain

import os
import re
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

src_test_list = os.path.join(os.path.expanduser('~'), 'src', 'fdo', 'test-lists',
                             'piglit-gen12-simics.txt')

subset = os.environ.get('SUBSET', None)

if subset:
    src_test_names = open(src_test_list).readlines()
    regex = re.compile(r'^(\d+)/(\d+)$')
    mo = regex.match(subset)
    assert mo
    part_num = int(mo.group(1))
    num_parts = int(mo.group(2))
    assert part_num > 0 and part_num <= num_parts
    num_per_group = len(src_test_names) // num_parts
    start_num = (part_num - 1) * num_per_group
    if part_num < num_parts:
        end_num = part_num * num_per_group
    else:
        end_num = len(src_test_list)
    test_names = src_test_names[start_num:end_num]

    tmp_test_list = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8')

    for line in test_names:
        tmp_test_list.write(line)
    tmp_test_list.flush()

    test_list = tmp_test_list.name
    log = os.path.join(log_dir, f'1k-{start_num:04d}-{end_num:04d}-{timenow}')
else:
    test_list = src_test_list
    log = os.path.join(log_dir, f'1k-{timenow}')

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
