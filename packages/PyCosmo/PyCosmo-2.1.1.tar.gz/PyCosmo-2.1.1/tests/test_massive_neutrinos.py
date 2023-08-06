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

HERE = os.path.dirname(os.path.abspath(__file__))


def _setup_cosmo(model, **kw):

    c = PyCosmo.build(model, **kw)
    c.set(
        pk_type="boltz",
        pk_nonlin_type=None,
        initial_conditions="class",
        recomb="class",
        recomb_dir=os.path.join(HERE, "comparison_files/class_comparison"),
        recomb_filename="3nus_006_00_thermodynamics.dat",
        table_size=5000,
        pk_norm_type="A_s",
        pk_norm=2.1e-9,
        boltzmann_rtol=1e-6,
        boltzmann_atol=1e-8,
    )

    return c


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_mnu():
    c = _setup_cosmo("mnulcdm", l_max=5, l_max_mnu=5, mnu_relerr=1e-4)
    return c


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_fast_mnuwcdm():
    return _setup_cosmo("mnuwcdm", l_max=3, l_max_mnu=3)


@pytest.fixture(scope="module")
def cosmo_fast_mnuwcdm_rsa():
    return _setup_cosmo("mnuwcdm", l_max=3, l_max_mnu=3, rsa=True)


def test_fields():
    c = PyCosmo.build("mnulcdm", l_max_mnu=3, l_max=3)
    c.set(pk_type="boltz", pk_nonlin_type=None)
    grid = np.array([-5, -4, -3, -2, -1, 0])
    fields = c.lin_pert.fields(k=0.1, grid=grid)

    assert len(fields.delta_nu_m) == len(grid)
    assert len(fields.u_nu_m) == len(grid)
    assert len(fields.sigma_nu_m) == len(grid)


def test_fields_rsa():
    c = PyCosmo.build("mnulcdm", l_max_mnu=3, l_max=3, rsa=True)
    c.set(pk_type="boltz", pk_nonlin_type=None)

    grid = np.array([-5, -4, -3, -2, -1, 0])
    fields = c.lin_pert.fields(k=0.1, grid=grid)

    assert len(fields.delta_nu_m) == len(grid)
    assert len(fields.u_nu_m) == len(grid)
    assert len(fields.sigma_nu_m) == len(grid)


@pytest.mark.slow
def test_boltzmann_mnu(cosmo_mnu):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_mnu.lin_pert.fields(grid=[-2], k=0.01)

    fields_to_be = np.array(
        [
            [-4.67324296e-01],
            [-1.27255065e02],
            [6.26552252e00],
            [-1.26854469e02],
            [6.26462246e00],
            [-4.46315481e-01],
            [-2.24841981e-04],
            [-4.50037564e-01],
            [-1.79312667e-02],
            [6.23954606e-05],
            [-5.30433194e-03],
            [-4.60532485e-04],
            [-4.70846394e-05],
            [-3.77962360e-03],
        ]
    )

    fields_mnu_to_be = np.array([[-1.75014577e01], [1.29922095e00], [7.51434809e-02]])

    assert np.allclose(fields._y[:14], fields_to_be, atol=0, rtol=6e-4)
    assert np.allclose(fields._y[-3:], fields_mnu_to_be, atol=0, rtol=6e-4)


@pytest.mark.slow
def test_boltzmann_mnuwcdm_fast(cosmo_fast_mnuwcdm):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_fast_mnuwcdm.lin_pert.fields(grid=[-5], k=0.01)

    fields_to_be = np.array(
        [
            [-4.80736246e-01],
            [-7.42048058e00],
            [1.43954421e00],
            [-7.14412994e00],
            [1.42178658e00],
            [-3.62616732e-02],
            [4.77418486e-01],
            [-4.39679669e-01],
            [-7.99664474e-04],
            [-4.38906242e-01],
            [-9.10700945e-02],
            [5.60680593e-04],
            [-3.65605229e-02],
            [-9.49325358e-02],
        ]
    )

    fields_mnu_to_be = np.array([[-1.76697028e00], [-0.09682157e00], [-0.11047227e00]])

    assert np.allclose(fields._y[:14], fields_to_be, atol=0, rtol=6e-4)
    assert np.allclose(fields._y[-3:], fields_mnu_to_be, atol=0, rtol=6e-4)


def test_boltzmann_mnuwcdm_fast_rsa(cosmo_fast_mnuwcdm_rsa):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_fast_mnuwcdm_rsa.lin_pert.fields(grid=[-5], k=0.01)

    fields_to_be = np.array(
        [
            [-4.80736246e-01],
            [-7.42048058e00],
            [1.43954421e00],
            [-7.14412994e00],
            [1.42178658e00],
            [-3.62616732e-02],
            [4.77418486e-01],
            [-4.39679669e-01],
            [-7.99664474e-04],
            [-4.38906242e-01],
            [-9.10700945e-02],
            [5.60680593e-04],
            [-3.65605229e-02],
            [-9.49325358e-02],
        ]
    )

    fields_mnu_to_be = np.array([[-1.76697029e00], [-0.09682158e00], [-0.11047227e00]])

    assert np.allclose(fields._y[:14], fields_to_be, atol=0, rtol=6e-4)
    assert np.allclose(fields._y[-3:], fields_mnu_to_be, atol=0, rtol=6e-4)
