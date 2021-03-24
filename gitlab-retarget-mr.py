#!/usr/bin/env python3
# Jordan Justen : this file is public domain

# This script helps a gitlab project change the default branch. After
# setting up a new default branch, most open merge requests will still
# have the old default branch set as the merge request target. This
# script finds all affected merge requests and changes the target
# branch.
description='Changes the target branch for open merge reqests'

import argparse
import gitlab
import re
import subprocess
import sys
import textwrap
import urllib.parse

class App:
    def __init__(self):
        self.parse_cmdline()
        self.get_url()
        self.run()

    def run(self):
        self.dry_run = self.args.dry_run

        input_project = self.project_path
        project_path = input_project.split('/')
        assert len(project_path) > 1
        groups = project_path[:-1]
        project = project_path[-1]

        gl_url = self.url_scheme + '://' + self.server

        if self.args.token is not None:
            self.token = self.args.token
        elif self.args.ask_token:
            import getpass
            token_url = gl_url + '/-/profile/personal_access_tokens'
            print("Enter api token from", token_url)
            self.token = getpass.getpass('Token:')
        else:
            self.token = None

        kwarg = {}
        if self.token is not None:
            kwarg['private_token'] = self.token
        gl = gitlab.Gitlab(gl_url, **kwarg)

        group = None
        for g in groups:
            if group is None:
                users = gl.users.list(username=g)
                if len(users) < 1:
                    group = gl.groups.get(g)
                else:
                    group = users[0]
            else:
                group = gl.groups.get(g, lazy=True)
            assert group is not None

        glp = None
        for p in group.projects.list(search=project):
            if p.name == project:
                glp = gl.projects.get(p.id)
                break
        assert glp is not None
        assert glp.path_with_namespace.lower() == input_project.lower()

        # Order by oldest updated first. This will mean the most
        # recently updated merge-requests will be changed last, and
        # therefore remain the most recently updated merge-requests.
        mrs = glp.mergerequests.list(state='opened', order_by='updated_at',
                                     sort='asc', lazy=True, all=True)
        mrs_to_retarget = []

        for mr in mrs:
            if mr.target_branch == self.args.old_target:
                mrs_to_retarget.append(mr)

        print(('Found {} merge requests that need to change target '
               'from {} to {}').format(
                   len(mrs_to_retarget),
                   self.args.old_target, self.args.new_target))
        for mr in mrs_to_retarget:
            # mr_str = 'mr-{0.iid} {0.title}'.format(mr)
            mr_str = mr.web_url
            if self.dry_run:
                print('Would retarget', mr_str)
            else:
                print('Retargeting', mr_str, end=' ')
                try:
                    edit_mr = glp.mergerequests.get(mr.iid, lazy=True)
                    edit_mr.target_branch = self.args.new_target
                    edit_mr.save()
                    print('[success]')
                except gitlab.exceptions.GitlabAuthenticationError:
                    print('[failed]')
                    if self.token is None:
                        print("You may need to provide a token to update "
                              "merge-requests")
                    else:
                        print("Your access token may not be able to edit "
                              "the merge-request!")
                    sys.exit(1)

    def get_url(self):
        if self.args.remote is not None:
            cmd = ['git', 'remote', 'get-url']
            cmd.append(self.args.remote)
            p = subprocess.run(cmd, capture_output=True)
            if p.returncode != 0:
                print('Unable to get url from git remote "{}"'.format(
                    self.args.remote))
                sys.exit(1)
            self.url = p.stdout.decode().strip()
        else:
            self.url = self.args.url

        if self.url.startswith('http'):
            p = urllib.parse.urlparse(self.url)
            self.url_scheme = p.scheme
            self.server = p.netloc
            self.project_path = p.path
        else:
            regex = re.compile('git@(?P<serv>.*):(?P<path>.*)')
            match_obj = regex.match(self.url)
            assert match_obj is not None
            self.url_scheme = 'https'
            self.server = match_obj.group('serv')
            self.project_path = match_obj.group('path')
        assert self.url is not None
        if self.project_path.endswith('.git'):
            self.project_path = self.project_path[:-4]
        self.project_path = self.project_path.lstrip('/')

    def parse_cmdline(self):
        p = argparse.ArgumentParser(
            description=description,
            epilog = textwrap.dedent(
                """\
                Usage examples:

                Diplay what merge requests need changes, but make no changes
                $ {0} --url=https://gitlab.com/username/reponame

                Diplay what merge requests need changes, but make no changes
                $ {0} --remote=origin

                Attempt to change all merge request targets from `foo` to `main`
                $ {0} --remote=origin --token=secret_token --old-branch=foo --do-it

                Attempt to change all merge request targets from `master` to `main`
                $ {0} --remote=origin --ask-token --do-it
                """).format(sys.argv[0]),
            formatter_class=argparse.RawDescriptionHelpFormatter)

        g = p.add_mutually_exclusive_group()
        g.add_argument('--dry-run', action='store_true', default=True,
                       help="Don't make any changes (this is the default)")
        g.add_argument('--do-it', action='store_false', dest='dry_run',
                       help="Attempt to make changes")

        g = p.add_mutually_exclusive_group(required=True)
        g.add_argument("--url", default=None,
                       help="Gitlab project url, "
                       "example: https://gitlab.com/group/repo")
        g.add_argument("--remote", default=None,
                       help="Find gitlab project url in git remote, "
                       "example: origin")

        g = p.add_mutually_exclusive_group()
        g.add_argument("--token", default=None,
                       help="Gitlab user personal token. "
                       "https://gitlab.com/-/profile/personal_access_tokens")
        g.add_argument("--ask-token", action='store_true',
                       help="Ask for the token at runtime")

        p.add_argument("--old-target",
                       default='master',
                       help="The old target branch name for merge-requests "
                       "(default: %(default)s)")
        p.add_argument("--new-target",
                       default='main',
                       help="The new target branch name for merge-requests "
                       "(default: %(default)s)")

        a = p.parse_args()

        def error(s):
            p.print_help()
            print(s)

        self.cmdline_parser = p
        self.args = a

if __name__ == "__main__":
    App()
