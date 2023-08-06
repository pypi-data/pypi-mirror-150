# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
# Copyright 2017 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


import os


from byov import subprocesses


import byoci


class Repository(object):
    """A facade for local git repositories.

    The command line tool (and its API) are used to reduce the coupling.
    """

    def __init__(self, location):
        self.location = os.path.abspath(location)

    def _run(self, args):
        return subprocesses.run(['git'] + args)

    def tip_commit_id(self):
        with byoci.working_directory(self.location):
            return self._run(['rev-parse', 'HEAD'])[1].strip()

    def create(self):
        return self._run(['init', self.location])

    # FIXME: Refactoring needed to better support multiple code hosting
    # providers (like launchpad and gitlab) by better separating project
    # (encompassing repositories) and branch -- vila 2018-07-25
    def create_from(self, existing, branch_name='master'):
        return self._run(['clone', '--branch', branch_name, existing,
                          self.location])

    def update(self, description, tree_update):
        from byoci.tests import fixtures
        with byoci.working_directory(self.location):
            fixtures.build_tree(tree_update)
            self._run(['add', '.'])
            return self._run(['commit', '-m', description])

    # FIXME: gitlab requires the branch name to hold the stem as it doesn't
    # support multiple repositories for a given project (like launchpad)
    # -- vila 2018-07-24
    def push(self, url, branch='master'):
        with byoci.working_directory(self.location):
            return self._run(['push', url, branch])

    def delete(self):
        with byoci.working_directory(self.location):
            return subprocesses.run(['rm', '-fr', self.location])

    def status(self):
        with byoci.working_directory(self.location):
            ret, out, err = self._run(['status', '--short'])
            return out

    def last_commit_msg(self):
        with byoci.working_directory(self.location):
            _, out, _ = self._run(['log', '-1'])
        lines = out.splitlines()
        # Forget first and last lines
        lines = lines[4:]
        return '\n'.join([l[4:] for l in lines])

    def switch(self, branch):
        with byoci.working_directory(self.location):
            return self._run(['checkout', '-b', branch])
