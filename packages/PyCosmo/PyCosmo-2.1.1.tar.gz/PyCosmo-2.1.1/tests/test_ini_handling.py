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


import pickle

from PyCosmo.ini_handling import Bunch


def test_bunch():
    data = dict(a=3, b=dict(c=4))
    x = Bunch(data)
    assert x.a == 3
    assert x.b.c == 4

    x.b.c = 5
    x.a = 4

    x.x = 4
    x.b.x = 4

    assert x.as_dict() == dict(a=4, x=4, b=dict(c=5, x=4))


def test_pickling():
    data = dict(a=3, b=dict(c=4))
    x = Bunch(data)

    bb = pickle.dumps(x)
    x = pickle.loads(bb)
    assert x.a == 3
    assert x.b.c == 4
