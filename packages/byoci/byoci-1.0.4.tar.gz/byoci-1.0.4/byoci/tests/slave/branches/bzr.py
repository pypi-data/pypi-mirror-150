# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
# Copyright 2016, 2017 Canonical Ltd.
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


class Branch(object):
    """A facade for local bzr branches.

    The command line tool (and its API) are used to reduce the coupling.
    """

    def __init__(self, location):
        self.location = os.path.abspath(location)

    def _run(self, args):
        return subprocesses.run(['bzr'] + args)

    def tip_commit_id(self):
        with byoci.working_directory(self.location):
            return self._run(['revision-info'])[1].split()[1].strip()

    def create(self):
        return self._run(['init', self.location])

    def create_from(self, existing):
        return self._run(['branch', existing, self.location])

    def update(self, description, tree_update):
        from byoci.tests import fixtures
        with byoci.working_directory(self.location):
            fixtures.build_tree(tree_update)
            self._run(['add'])
            return self._run(['commit', '-m', description])

    def push(self, url):
        with byoci.working_directory(self.location):
            return self._run(['push', url])

    def delete(self):
        with byoci.working_directory(self.location):
            return subprocesses.run(['rm', '-fr', self.location])

    def status(self):
        with byoci.working_directory(self.location):
            ret, out, err = self._run(['status'])
            return out

    def last_commit_msg(self):
        with byoci.working_directory(self.location):
            _, out, _ = self._run(['log', '-l1', '--short'])
        lines = out.splitlines()
        # Forget first and last lines
        lines = lines[1:-1]
        return '\n'.join([l[6:] for l in lines])
