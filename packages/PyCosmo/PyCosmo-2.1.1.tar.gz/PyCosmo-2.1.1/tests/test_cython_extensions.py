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

from PyCosmo.cython.halo_integral import _integral_halo as cython_integral_halo
from PyCosmo.NonLinearPerturbationMead import integral_halo as numpy_integral_halo


def test_integral_halo():

    nk = 300
    na = 200
    nm = 100

    k = 0.7 * 10 ** np.linspace(-3, 4, nk)
    a = np.exp(np.linspace(-1, 0, na))
    nu_range = 10 ** np.linspace(-100, 2, nm)
    m_msun = 10 ** np.linspace(-100, 20, na * nm).reshape(na, nm)

    rv_mpc = 10 ** np.linspace(-55, 2, na * nm).reshape(na, nm)

    c = np.linspace(3, 2000, na * nm).reshape(na, nm)
    f = np.linspace(0, 2.5, nm)

    eta = np.repeat(0.3333, na)

    i0 = numpy_integral_halo(k, m_msun, nu_range, rv_mpc, c, a, f, eta)
    i1 = cython_integral_halo(k, m_msun, nu_range, rv_mpc, c, a, f, eta, adaptive=0)
    i2 = cython_integral_halo(k, m_msun, nu_range, rv_mpc, c, a, f, eta, adaptive=1)

    assert i0.shape == i1.shape == i2.shape

    assert np.all(np.abs(i1 - i0) < 6e-13 * np.abs(i0))
    assert np.all(np.abs(i2 - i0) < 8e-12 * np.abs(i0))
