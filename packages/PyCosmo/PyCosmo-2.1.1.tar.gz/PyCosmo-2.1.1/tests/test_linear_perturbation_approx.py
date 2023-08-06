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
from functools import partial

import numpy as np
import pytest

import PyCosmo
from PyCosmo._Util import relative_differences

HERE = os.path.dirname(os.path.abspath(__file__))

j = partial(os.path.join, HERE)


@pytest.fixture
def cosmo():
    config_name = j("param_files/PyCosmo_test1_param.ini")
    cosmo = PyCosmo.build("wcdm")
    cosmo.load_params(config_name)
    yield cosmo


@pytest.fixture
def cosmo_LCDM():
    config_name = j("param_files/PyCosmo_test5_param.ini")
    cosmo = PyCosmo.build("lcdm")
    cosmo.load_params(config_name)
    yield cosmo


@pytest.fixture
def cosmo_mnulcdm():
    cosmo = PyCosmo.build("mnulcdm", l_max=3, l_max_mnu=3)
    cosmo.set(
        pk_type="EH",
        N_massive_nu=1.0,
        N_massless_nu=2.0,
        massive_nu_total_mass=0.1,
        T_mnu=0.713765855503608,
    )
    yield cosmo


@pytest.fixture
def data_growth():
    data_file = j("comparison_files/bench_growth.txt")
    yield np.loadtxt(data_file)


@pytest.fixture
def data2():
    yield np.loadtxt(j("comparison_files/pkicosmo3.txt"))


@pytest.fixture
def data3():
    yield np.loadtxt(j("comparison_files/pk_BBKS_icosmo.txt"))


def test_growth_simple(cosmo):
    """Basic set of tests that makes sure that the right types of outputs are
    produced and that some specific values are in agreement with
    previous calculations to numerical precision.
    """
    growth = cosmo.lin_pert.growth_a(a=0.5)
    assert len(growth) == 1
    assert np.isclose(growth[0], 0.61574353, atol=0)


def test_growth_hyper_simple(cosmo_LCDM):
    """Basic set of tests that makes sure that the right types of outputs are
    produced and that some specific values are in agreement with
    previous calculations to numerical precision.
    """
    growth = cosmo_LCDM.lin_pert._growth_hyper_a(a=0.5)
    assert len(growth) == 1.0
    assert np.allclose(growth, 0.61193192, atol=0, rtol=1e-6)


def test_growth_hyper(cosmo_LCDM):
    """Compare the growth factor computed by integrating the diffential equation
    to that from the analytical hypergeometric function for LCDM
    """
    a = np.logspace(-1.0, 0.0)
    # TODO: difference with hypergeometric function expected to be smaller, need to
    # check
    assert np.allclose(
        cosmo_LCDM.lin_pert.growth_a(a=a),
        cosmo_LCDM.lin_pert._growth_hyper_a(a=a),
        rtol=3e-3,
        atol=0,
    )


def test_growth(cosmo, data_growth):
    """This function has been written to test the calculation of
    the growth factor in PyCosmo
    """
    a = data_growth[:, 0]
    growth = data_growth[:, 2]
    assert (relative_differences(cosmo.lin_pert.growth_a(a=a), growth) <= 2.3e-3).all()

    # Case of norm=1 (D=a in case of matter-dominated Universe)
    cosmo.set(suppress_rad=True)
    cosmo.set(omega_m=1.0, omega_l=0.0, flat_universe=False)
    assert (relative_differences(cosmo.lin_pert.growth_a(a=a, norm=1), a) <= 1e-4).all()


def test_transfer_EH(cosmo):
    """Tests the implementation of the transfer function as described in
    Eisenstein & Hu, 1998, ApJ, 511, 5"""

    t_eh_c = np.loadtxt(j("comparison_files/transfer_EH_test1_c.txt"))

    ks = np.logspace(-4, 2, 1000)

    t_eh = cosmo.lin_pert._transfer_EH(ks)

    assert np.allclose(t_eh, t_eh_c, atol=0, rtol=2e-4)


def test_pk_EH_icosmo(cosmo, data2):
    """Tests the power spectrum calculated as described in
    Eisenstein & Hu, 1998, ApJ, 511, 5, in comparison with iCosmo"""

    ks = data2[:, 0] * 0.7
    pk_EH = cosmo.lin_pert.powerspec_a_k(a=1.0, k=ks)[:, 0]
    pk_EH_icosmo = data2[:, 1]
    pk_EH_icosmo = pk_EH_icosmo / (0.7**3)
    assert (relative_differences(pk_EH, pk_EH_icosmo) <= 0.002).all()


def test_pk_BBKS_icosmo(cosmo, data3):
    """Test the implementation of the transfer function as summarised in
    Peacock & Dodds"""

    cosmo.set(pk_type="BBKS")

    cosmo.set(omega_m=0.3, omega_l=0.7, flat_universe=False)

    ks = data3[:, 0] * 0.7
    pk_BBKS = cosmo.lin_pert.powerspec_a_k(a=1.0, k=ks)[:, 0]
    pk_BBKS_icosmo = data3[:, 1]
    pk_BBKS_icosmo = pk_BBKS_icosmo / (0.7**3)

    assert (relative_differences(pk_BBKS, pk_BBKS_icosmo) <= 9.0e-6).all()


def test_powerspec_api(cosmo):
    a = [0.1, 0.5, 1]
    ks = [0.1, 0.5, 0.9]
    p1 = cosmo.lin_pert.powerspec_a_k(a=a, k=ks, diag_only=False)
    p2 = cosmo.lin_pert.powerspec_a_k(a=a, k=ks, diag_only=True)
    assert np.allclose(np.diag(p1), p2)


def test_growth_EH_mnu_shape(cosmo_mnulcdm):

    avec = np.array([0.09, 0.2, 0.5])
    kvec = np.array([0.01, 1])

    assert cosmo_mnulcdm.lin_pert.growth_a(avec, kvec, diag_only=False).shape == (
        len(kvec),
        len(avec),
    )

    assert cosmo_mnulcdm.lin_pert.growth_a(0.1, kvec, diag_only=False).shape == (
        len(kvec),
        1,
    )

    assert cosmo_mnulcdm.lin_pert.growth_a(avec, [0.1], diag_only=False).shape == (
        1,
        len(avec),
    )

    assert cosmo_mnulcdm.lin_pert.growth_a(avec, avec, diag_only=True).shape == (
        len(avec),
    )


def test_growth_EH_shape(cosmo):

    cosmo.set(pk_type="EH")

    avec = np.array([0.1, 0.2, 0.5])
    kvec = np.array([0.01, 1])

    assert cosmo.lin_pert.growth_a(avec, kvec, diag_only=False).shape == (
        len(kvec),
        len(avec),
    )

    assert cosmo.lin_pert.growth_a(0.1, kvec, diag_only=False).shape == (
        len(kvec),
        1,
    )

    assert cosmo.lin_pert.growth_a(avec, [0.1], diag_only=False).shape == (
        1,
        len(avec),
    )

    assert cosmo.lin_pert.growth_a(avec, 0.1, diag_only=False).shape == (len(avec),)

    assert cosmo.lin_pert.growth_a(avec, None, diag_only=False).shape == (len(avec),)

    assert cosmo.lin_pert.growth_a(avec, avec, diag_only=True).shape == (len(avec),)


def test_powerspec_EH_mnu(cosmo_mnulcdm, cosmo_LCDM):

    cosmo_mnulcdm.set(N_massive_nu=1.0)
    assert np.isclose(
        cosmo_mnulcdm.lin_pert.powerspec_a_k(a=0.5, k=0.1)[0][0],
        3557.9565084917294,
        atol=0,
    )

    assert np.allclose(
        cosmo_mnulcdm.lin_pert.powerspec_a_k(a=[0.5, 1], k=[0.1, 0.2, 0.3]),
        np.array(
            [
                [3557.95650849, 9484.82328108],
                [1008.47564737, 2688.09477674],
                [444.69466134, 1185.29796448],
            ]
        ),
        atol=0,
    )
    assert (
        cosmo_mnulcdm.lin_pert.powerspec_a_k(a=[0.5, 1], k=[0.1, 0.2, 0.3]).shape
        == cosmo_LCDM.lin_pert.powerspec_a_k(a=[0.5, 1], k=[0.1, 0.2, 0.3]).shape
    )

    assert np.allclose(
        cosmo_mnulcdm.lin_pert.powerspec_a_k(a=[0.5, 1], k=[0.1, 0.2], diag_only=True),
        np.array(
            [3557.95650849, 2688.09477674],
        ),
        atol=0,
    )
