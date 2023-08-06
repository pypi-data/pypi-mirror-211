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

__author__ = "Andrina"

import numpy as np
import pytest

import PyCosmo

"""
Test the NonLinear perturbation module.
"""

config_icosmo_w095 = "tests.param_files.PyCosmo_icosmo_w-095_param"


@pytest.fixture
def halofit_w1(data_path):
    c = PyCosmo.build()
    c.load_params(data_path("param_files/PyCosmo_icosmo_w-1_param.ini"))
    yield c.nonlin_pert


@pytest.fixture
def halofit_w095(data_path):
    c = PyCosmo.build("wcdm")
    c.load_params(data_path("param_files/PyCosmo_icosmo_w-095_param.ini"))
    yield c.nonlin_pert


@pytest.mark.slow
def test_halofit(halofit_w1, halofit_w095, data_path):
    """Tests the implementation of the halofit fitting function as described in
    Smith et al., 2003, MNRAS, 341, 1311"""

    test1 = np.loadtxt(
        data_path("comparison_files/pk_icosmo_w-1_z0.txt"), usecols=(0, 1)
    )
    ks1 = test1[:, 0]
    pk_nonlin_icosmo1 = test1[:, 1]
    test2 = np.loadtxt(
        data_path("comparison_files/pk_icosmo_w-095_z0.txt"), usecols=(0, 1)
    )
    ks2 = test2[:, 0]
    pk_nonlin_icosmo2 = test2[:, 1]
    test3 = np.loadtxt(
        data_path("comparison_files/pk_icosmo_w-1_z2.txt"), usecols=(0, 1)
    )
    ks3 = test3[:, 0]
    pk_nonlin_icosmo3 = test3[:, 1]
    test4 = np.loadtxt(
        data_path("comparison_files/pk_icosmo_w-095_z2.txt"), usecols=(0, 1)
    )
    ks4 = test4[:, 0]
    pk_nonlin_icosmo4 = test4[:, 1]

    h_w1 = halofit_w1._params.h
    h_w095 = halofit_w095._params.h

    pk_nonlin1 = halofit_w1.powerspec_a_k(1.0, ks1 * h_w1)
    pk_nonlin1 = np.reshape(pk_nonlin1, pk_nonlin1.shape[0])
    pk_nonlin2 = halofit_w095.powerspec_a_k(1.0, ks2 * h_w095)
    pk_nonlin2 = np.reshape(pk_nonlin2, pk_nonlin2.shape[0])
    pk_nonlin3 = halofit_w1.powerspec_a_k(1.0 / 3.0, ks3 * h_w1)
    pk_nonlin3 = np.reshape(pk_nonlin3, pk_nonlin3.shape[0])
    pk_nonlin4 = halofit_w095.powerspec_a_k(1.0 / 3.0, ks4 * h_w095)
    pk_nonlin4 = np.reshape(pk_nonlin4, pk_nonlin4.shape[0])

    assert np.allclose(pk_nonlin1, pk_nonlin_icosmo1 * h_w1**-3, atol=0.0, rtol=2e-3)
    assert np.allclose(
        pk_nonlin2, pk_nonlin_icosmo2 * h_w095**-3, atol=0.0, rtol=2e-3
    )
    assert np.allclose(pk_nonlin3, pk_nonlin_icosmo3 * h_w1**-3, atol=0.0, rtol=7e-3)
    assert np.allclose(
        pk_nonlin4, pk_nonlin_icosmo4 * h_w095**-3, atol=0.0, rtol=8e-3
    )


def test_halofit_regression(halofit_w1, halofit_w095):
    """Tests the implementation of the halofit fitting function as described in
    Smith et al., 2003, MNRAS, 341, 1311"""

    k_vec = [0.1, 0.3, 0.5, 0.9]
    a_vec = [0.2, 0.5, 1.0]

    pk = halofit_w1.powerspec_a_k(a_vec, k_vec)
    tobe = np.array(
        [
            [+6.51110e02, +3.72388e03, +9.77144e03],
            [+8.77835e01, +6.49897e02, +2.32338e03],
            [+3.13292e01, +3.20532e02, +1.42355e03],
            [+9.59804e00, +1.59371e02, +8.03329e02],
        ]
    )

    assert np.allclose(pk, tobe, atol=0)
    pk = halofit_w095.powerspec_a_k(a_vec, k_vec)
    tobe = np.array(
        [
            [+6.67778e02, +3.76848e03, +9.75374e03],
            [+9.01078e01, +6.59352e02, +2.32541e03],
            [+3.22238e01, +3.26224e02, +1.42984e03],
            [+9.93275e00, +1.62791e02, +8.10281e02],
        ]
    )

    assert np.allclose(pk, tobe, atol=0)


def test_powerspec_api(halofit_w1):
    pk = halofit_w1.powerspec_a_k([0.2, 0.3], [0.1, 0.2, 0.5], diag_only=False)
    assert pk.shape == (3, 2)
    p1 = halofit_w1.powerspec_a_k([0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=False)
    assert p1.shape == (3, 3)
    p2 = halofit_w1.powerspec_a_k([0.2, 0.3, 0.5], [0.1, 0.2, 0.5], diag_only=True)
    assert p2.shape == (3,)

    assert np.allclose(np.diag(p1), p2)
