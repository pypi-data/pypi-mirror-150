#
# pagemarks - Free, git-backed, self-hosted bookmarks
# Copyright (c) 2019-2021 the pagemarks contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License, version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/gpl.html>.
#

import json
import unittest

from pagemarks.commands.locate import CmdLocate
from pagemarks.framework.cmdline import CmdLine



class LocateTestCase(unittest.TestCase):

    # We read the mapping from URL to filename from a file, so that the same mapping is guaranteed in JavaScript.
    def test_url_to_filename_from_spec_file(self):
        with open('test/url_to_filename.json', 'r', encoding='utf-8') as specfile:
            spec = json.load(specfile)
        for url in spec:
            under_test = CmdLocate(CmdLine(), url)
            actual = under_test.url_to_filename()
            expected = spec[url]
            self.assertEqual(expected, actual)
