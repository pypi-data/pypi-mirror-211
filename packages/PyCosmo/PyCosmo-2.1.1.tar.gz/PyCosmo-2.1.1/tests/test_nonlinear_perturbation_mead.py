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


import os

import numpy as np
import pytest

import PyCosmo
from PyCosmo._Util import relative_differences

# for regression tests: format all array outputs as follows:
np.set_printoptions(formatter={"all": lambda x: "%+.5e" % x})

HERE = os.path.dirname(os.path.abspath(__file__))

limit2 = 6.0e-3  # strong limit 2 EH


@pytest.fixture
def cosmo():
    cosmo = PyCosmo.build()
    cosmo.load_params(os.path.join(HERE, "param_files", "PyCosmo_Mead_param.ini"))
    yield cosmo


def test_0(cosmo):
    assert cosmo.params.pk_nonlin_type == "mead"


def test_params(cosmo):
    assert cosmo.background.H(a=1) == 70.0


def test_pk(cosmo):
    pk_mead = np.genfromtxt(os.path.join(HERE, "power.dat"))
    h = cosmo.params.h

    ks = pk_mead[:, 0] * h

    pk_mead_tobe = 2.0 * np.pi**2 * pk_mead[:, 2] / pk_mead[:, 0] ** 3 / h**3

    z = np.array([0.267])
    pk_hm_0 = cosmo.nonlin_pert.powerspec_a_k(1.0 / (1 + z), ks)
    maxtol = np.max(relative_differences(pk_hm_0.flatten(), pk_mead_tobe))
    assert maxtol <= limit2

    pk_mead_tobe = 2.0 * np.pi**2 * pk_mead[:, 3] / pk_mead[:, 0] ** 3 / h**3
    z = np.array([0.533333])
    pk_hm_1 = cosmo.nonlin_pert.powerspec_a_k(1.0 / (1 + z), ks)
    maxtol = np.max(relative_differences(pk_hm_1.flatten(), pk_mead_tobe))
    assert maxtol <= limit2

    z = np.array([0.267, 0.53333])
    pk_hm = cosmo.nonlin_pert.powerspec_a_k(1.0 / (1 + z), ks)

    pk_mead_tobe = 2.0 * np.pi**2 * pk_mead[:, [2, 3]] / pk_mead[:, [0]] ** 3 / h**3
    maxtol = np.max(relative_differences(pk_hm, pk_mead_tobe))
    assert maxtol <= limit2

    pk_with_invalid = cosmo.nonlin_pert.powerspec_a_k([-1, 0.1, 0.5, 2.0], [1, 2, 3])
    assert np.all(np.isnan(pk_with_invalid[:, 0]))  # negative
    assert np.all(np.isnan(pk_with_invalid[:, 1]))  # redshift to high
    assert not np.any(np.isnan(pk_with_invalid[:, 2]))  # valid
    assert np.all(np.isnan(pk_with_invalid[:, 3]))  # larger than 1


def test_cm(cosmo):

    m_grid0 = np.append([1e-300], 10 ** np.linspace(-250, 20, 10))
    m_grid1 = 50 * m_grid0
    m_grid = np.vstack((m_grid0[None, :], m_grid1[None, :]))

    a0 = 0.4
    s0x = cosmo.nonlin_pert.cm(m_grid0, a0)

    a1 = 0.8
    s1x = cosmo.nonlin_pert.cm(m_grid1, a1)

    sfull = cosmo.nonlin_pert.cm(m_grid, (a0, a1))
    assert np.allclose(np.hstack((s0x, s1x)), sfull)


def test_sigma8_scaling(cosmo):
    a_grid = 10 ** np.linspace(-4, 0, 20)
    a_grid = a_grid[a_grid >= 5e-2]
    # a_grid = a_grid[a_grid > 5e-2]
    sigma8s = cosmo.nonlin_pert.sigma8_a(a_grid)
    growths = cosmo.nonlin_pert._tables.growth_tab_a(a_grid)
    sfracs = sigma8s[1:] / sigma8s[:-1]
    growthfacs = growths[1:] / growths[:-1]
    assert np.max(np.abs(sfracs - growthfacs)) < 1e-8


def test_sigma_scaling(cosmo):
    a_grid = 10 ** np.linspace(-4, 0, 20)
    a_grid = a_grid[a_grid > 5e-2]

    m_grid = np.append([1e-300], 10 ** np.linspace(-250, 10, 10))

    # use exact sigma computations here
    sigmas = [cosmo.nonlin_pert._sigma(m_grid, a)[:, None] for a in a_grid]
    sigmas = np.hstack(sigmas)

    sfracs = sigmas[:, 1:] / sigmas[:, 0][:, None]

    growths = cosmo.nonlin_pert._tables.growth_tab_a(a_grid)
    growthfacs = growths[1:] / growths[0]

    assert np.max(np.abs((sfracs - growthfacs) / growthfacs)) < 8e-5


def test_sigma(cosmo):

    m_grid0 = np.append([1e-300], 10 ** np.linspace(-250, 10, 10))
    m_grid1 = 50 * m_grid0
    m_grid = np.vstack((m_grid0[None, :], m_grid1[None, :]))

    a_grid = 10 ** np.linspace(-50, 0, 20)
    a_grid = a_grid[a_grid > 5e-2]
    for a0 in a_grid:
        s0 = cosmo.nonlin_pert._sigma(m_grid0, a0)
        s0x = cosmo.nonlin_pert.sigma(m_grid0, a0)
        assert np.allclose(s0x[:, 0], s0)

    a0 = 0.4
    s0 = cosmo.nonlin_pert._sigma(m_grid0, a0)
    s0x = cosmo.nonlin_pert.sigma(m_grid0, a0)

    assert np.allclose(s0x[:, 0], s0)

    a1 = 0.8
    s1 = cosmo.nonlin_pert._sigma(m_grid1, a1)
    s1x = cosmo.nonlin_pert.sigma(m_grid1, a1)

    assert np.allclose(s1x[:, 0], s1)

    sfull = cosmo.nonlin_pert.sigma(m_grid, (a0, a1))
    assert np.allclose(np.hstack((s0x, s1x)), sfull)


def test_nu(cosmo):
    p = cosmo.nonlin_pert

    nu = np.array(
        [
            +1.89373e-02,
            +1.89853e-02,
            +1.91961e-02,
            +1.95860e-02,
            +2.03055e-02,
            +2.16506e-02,
            +2.42691e-02,
            +2.98781e-02,
            +4.48857e-02,
            +1.22103e-01,
        ]
    )

    a0 = 0.5
    m0 = p.nu2mass(nu, a0)
    m0_tobe = np.array(
        [
            [
                +0.00000e00,
                +4.75725e-221,
                +4.78697e-194,
                +4.90784e-167,
                +4.95236e-140,
                +5.01680e-113,
                +5.08476e-86,
                +5.14300e-59,
                +5.20927e-32,
                +5.27434e-05,
            ]
        ]
    )
    assert np.allclose(m0, m0_tobe)

    a1 = 0.7
    m1 = p.nu2mass(nu, a1)

    m1_tobe = np.array(
        [
            [
                +7.54945e-83,
                +1.98750e-82,
                +1.22572e-80,
                +1.49567e-77,
                +1.68024e-72,
                +9.37311e-65,
                +9.70321e-54,
                +2.84688e-39,
                +1.28203e-21,
                +2.42392e-01,
            ]
        ]
    )

    assert np.allclose(m1, m1_tobe)

    mfull = p.nu2mass(nu, [a0, a1])
    assert np.allclose(m0, mfull[0, :])
    assert np.allclose(m1, mfull[1, :])
