# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

import PyCosmo
from PyCosmo.Cosmo import Cosmo


@pytest.fixture
def cosmo():
    return PyCosmo.build()


def test_print_params(cosmo, regtest):
    cosmo.print_params(inc_internal=True, file=regtest)


class _TestCosmo(object):
    def setup(self):
        self.cosmo = PyCosmo.build()

    def test_print_cosmo(self):
        # Not really a unit test. just calling the function as sanity check

        self.cosmo.print_params(inc_consts=True)

    def test_default_param_file(self):
        cosmo = Cosmo()
        assert cosmo.paramfile == Cosmo._DEFAULT_PARAM_FILE

    def test_custom_param_file(self):
        paramfile = "tests.param_files.PyCosmo_test1_param"
        cosmo = Cosmo(paramfile)
        assert cosmo.paramfile == paramfile
