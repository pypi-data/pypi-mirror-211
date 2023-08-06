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

import numpy as np

from PyCosmo import _Util


def test_check_a_ode():
    a = np.arange(10)

    a_sort, ind_unsort = _Util._check_a_ode(a)
    assert a_sort is not None
    assert ind_unsort is not None
    assert np.all(a == a_sort)

    a_sort, ind_unsort = _Util._check_a_ode(a[::-1])
    assert a_sort is not None
    assert ind_unsort is not None
    assert np.all(a == a_sort)
    assert np.all(a[::-1] == ind_unsort)

    np.random.seed(42)
    for _ in range(100):
        np.random.shuffle(a)
        a_sort, ind_unsort = _Util._check_a_ode(a)
        assert np.all(a_sort[ind_unsort] == a)
