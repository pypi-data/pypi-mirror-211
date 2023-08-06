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

"""
Test the Background module.

"""
import os

import numpy as np
import pytest

import PyCosmo
from PyCosmo._Util import relative_differences

limit1 = 1.0e-5  # strong limit !!! NEEDED TO SOFTEN - NEED TO COME BACK TO !!!
limit2 = 1.0e-3  # weaker limit

testfile1 = "comparison_files/Bench_background.txt"
testfile2 = "comparison_files/Bench_background_testchi.txt"
testfile3 = "comparison_files/da_kpositive.txt"
testfile4 = "comparison_files/da_knegative.txt"


def _get_abspath(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


input_LCDM = _get_abspath("param_files/PyCosmo_icosmo_w-1_param.ini")


@pytest.fixture
def cosmo_LCDM():
    cosmo = PyCosmo.build()
    cosmo.load_params(input_LCDM)
    return cosmo


@pytest.fixture
def data():
    yield np.loadtxt(_get_abspath(testfile1))


@pytest.fixture
def data2():
    yield np.loadtxt(_get_abspath(testfile2))


@pytest.fixture
def data3():
    yield np.loadtxt(_get_abspath(testfile3))


@pytest.fixture
def data4():
    yield np.loadtxt(_get_abspath(testfile4))


def test_H(background):
    assert background.H(1.0) == 70.0


def test_H_LCDM(cosmo_LCDM):
    assert cosmo_LCDM.background.H(1.0) == 70.0
    assert relative_differences(cosmo_LCDM.background.H(0.5), 123.27312453) <= limit1


def test_angular_diameter_distance(background, data):
    """Basic set of tests that makes sure that the right types of outputs are
    produced and that some specific values are in agreement with
    previous calculations to numerical precision.
    """
    # print "Angular diameter distance at a = 0.4:"
    dist = background.dist_ang_a(a=0.4)
    assert relative_differences(dist, 1727.4757378121526) <= limit1

    # print "Angular diameter distance given all a values:"
    assert (
        relative_differences(data[1:, 3], background.dist_ang_a(a=data[1:, 0]))
        <= limit2
    ).all()  # limit1 doesn't pass!!!


def test_luminosity_distance(background, data):
    """Basic set of tests that makes sure that the right types of outputs are
    produced and that some specific values are in agreement with
    previous calculations to numerical precision.
    """
    # print "Luminosity distance at a = 0.6 and 0.8"
    dist = background.dist_lum_a(a=[0.6, 0.8])
    assert len(dist) == 2
    assert (relative_differences(dist[0], 3976.8514755670294) <= limit1).all()
    assert (relative_differences(dist[1], 1253.7370688034034) <= limit1).all()

    # print "Luminosity distance given all a values:"
    assert (
        relative_differences(data[1:, 2], background.dist_lum_a(a=data[1:, 0]))
        <= limit2
    ).all()  # limit1 doesn't pass!!!

    # Test the relation between luminosity distance and angular diameter distance,
    # according to eq.(21) in Section 1.3 of the PyCosmo notes.
    a = data[2:, 0]
    d_A = background.dist_ang_a(a=a)
    d_L = background.dist_lum_a(a=a)
    assert (relative_differences(d_A / (a * a), d_L) <= limit1).all()


def test_transverse_comoving_distance(cosmo, data, data3, data4):
    """
    Test the relation between transverse comoving distance (r) and Angular diameter
    (d_A) and Luminosity distance (l_A), according to d_A = (a*a)d_L = ar (eq.(21) in
    Section 1.3 of the PyCosmo notes), at different speed options.
    """
    a = data[7:, 0]
    background = cosmo.background
    d_A = background.dist_ang_a(a=a)
    d_L = background.dist_lum_a(a=a)
    r = background.dist_trans_a(a=a)
    r_f = background.dist_trans_a(a=a)

    assert relative_differences(r, d_A / a <= limit1).all()
    assert relative_differences(r, d_L / a <= limit1).all()
    assert relative_differences(r_f, d_A / a <= limit1).all()
    assert relative_differences(r_f, d_L / a <= limit1).all()

    # Make sure that the different speed options give consistent results
    assert (relative_differences(r, r_f) <= limit1).all()

    # Test the case omega_k>0
    cosmo.set(
        omega_suppress=False,
        suppress_rad=True,
        omega_l=0.7,
        flat_universe=False,
        omega_m=0.2,
    )

    DA_pycosmo = cosmo.background.dist_trans_a(a=data3[1:, 0])
    DA_icosmo = data3[1:, 3]
    z = data3[1:, 1]

    pycosmo_var = np.arcsinh(DA_pycosmo / (cosmo.params.rh / cosmo.params.sqrtk)) * (
        cosmo.params.rh / cosmo.params.sqrtk
    )
    icosmo_var = np.arcsinh(DA_icosmo * (1 + z) / 13543.243) * 13543.243

    assert (relative_differences(pycosmo_var, icosmo_var) <= limit1).all()

    # Test the case omega_k<0
    cosmo.set(
        omega_suppress=False,
        suppress_rad=True,
        omega_l=0.7,
        flat_universe=False,
        omega_m=0.5,
    )
    cosmo.print_params()
    assert cosmo.background._omega_r_a(a=1) == 0.0

    DA_pycosmo = cosmo.background.dist_trans_a(a=data4[1:, 0])
    DA_icosmo = data4[1:, 3]
    z = data4[1:, 1]

    pycosmo_var = np.arcsin(DA_pycosmo / (cosmo.params.rh / cosmo.params.sqrtk)) * (
        cosmo.params.rh / cosmo.params.sqrtk
    )
    icosmo_var = np.arcsin(DA_icosmo * (1 + z) / 9576.5188) * 9576.5188

    assert (relative_differences(pycosmo_var, icosmo_var) <= limit1).all()


def test_tau(background):
    """simple test of tau
    !!!!NEED TO CONFIRM THE VALUE AT a = 0.4"""
    tau = background.tau(0.4)
    assert len(tau) == 1
    assert (relative_differences(tau[0], 8.98551196037e-07) <= limit1).all()


def test_recres(background):
    """simple test of results from recfast
    !!!!NEED TO CONFIRM THE VALUE AT a = 0.4"""
    Xe_H_a = background._rec.xe_h_a([0.4])
    Xe_He_a = background._rec.xe_he_a([0.4])
    Xe_a = background._rec.xe_a([0.4])
    assert len(Xe_H_a) == 1
    assert len(Xe_He_a) == 1
    assert len(Xe_a) == 1
    assert (relative_differences(Xe_H_a[0], 0.000191792279334) <= limit1).all()
    assert (relative_differences(Xe_a[0], 0.000191791748207) <= limit1).all()


def _test_H_a_speed_options(background):
    """
    test to make sure the different speed options give consistent results
    !!!!NEED TO CONFIRM THE VALUE AT a = 0.4
    """
    res1 = background._H2_H02_Omegal_a(a=0.4, override_speed="slow_all")
    res2 = background._H2_H02_Omegal_a(
        a=[0.4], override_speed="fast_all"
    )  # !!Issue with []
    res3 = background._H2_H02_Omegal_a(a=0.4, override_speed="slow")
    res4 = background._H2_H02_Omegal_a(
        a=[0.4], override_speed="fast"
    )  # !!Issue with []
    res_base = 0.803038672023  # !!! Check NEED EXACT SOLUTION!!!
    assert len(res1) == 1
    assert len(res2) == 1
    assert len(res3) == 1
    assert len(res4) == 1

    assert (relative_differences(res1[0], res_base) <= limit1).all()
    assert (relative_differences(res2[0], res_base) <= limit1).all()
    assert (relative_differences(res3[0], res_base) <= limit1).all()
    assert (relative_differences(res4[0], res_base) <= limit1).all()


def _test_dist_rad_speed_options(background):
    """
    test to make sure the different speed options give consistent results
    !!!!NEED TO CONFIRM THE VALUE AT a = 0.4
    """
    res1 = background.dist_rad_a(a=0.4, override_speed="slow_all")
    res2 = background.dist_rad_a(a=0.4, override_speed="fast_all")  # !!Issue with []
    res3 = background.dist_rad_a(a=0.4, override_speed="slow")
    res4 = background.dist_rad_a(a=0.4, override_speed="fast")  # !!Issue with []
    res_base = 4318.688087604477  # !!! Check NEED EXACT SOLUTION!!!
    assert len(res1) == 1
    assert len(res2) == 1
    assert len(res3) == 1
    assert len(res4) == 1
    assert (relative_differences(res1[0], res_base) <= limit1).all()
    assert (relative_differences(res2[0], res_base) <= limit1).all()
    assert (relative_differences(res3[0], res_base) <= limit1).all()
    assert (relative_differences(res4[0], res_base) <= limit1).all()


def test_dist_rad_a(cosmo, data, data2):
    # print "chi at a = 0.4:"
    chi = cosmo.background.dist_rad_a(a=0.4)
    # limit1 doesn't pass!!!
    assert relative_differences(chi, 4318.68620678539) <= limit1

    return

    # OBSOLETE:
    # Make sure that the different speed options give consistent results
    chi_slow = cosmo.background.dist_rad_a(a=0.4, override_speed="slow")
    chi_fast = cosmo.background.dist_rad_a(a=0.4, override_speed="fast")
    chi_slow_all = cosmo.background.dist_rad_a(a=0.4, override_speed="slow_all")
    chi_fast_all = cosmo.background.dist_rad_a(a=0.4, override_speed="fast_all")
    assert (relative_differences(chi_slow, chi_fast) <= limit1).all()
    assert (relative_differences(chi_slow_all, chi_fast_all) <= limit1).all()
    assert (relative_differences(chi_slow, chi_slow_all) <= limit1).all()
    assert (relative_differences(chi_fast, chi_fast_all) <= limit1).all()
    # Make sure that different configuration values (varying h) give consistent results

    hvalues = np.arange(0.4, 0.9, 0.1)
    for k, h in enumerate(hvalues):
        cosmo.set(h=h)
        chi = cosmo.background.dist_rad_a(a=data[1:, 0])
        chi_icosmo = data2[1:, k]
        assert (relative_differences(chi, chi_icosmo) <= limit2).all()


def test_eta(cosmo_LCDM):
    """simple test of eta
    !!!!NEED TO CONFIRM THE VALUE AT a = 0.4"""

    cosmo = cosmo_LCDM
    cosmo.set(
        h=0.67,
        N_massless_nu=3.0,
        omega_m=0.3,
        omega_b=0.03,
        flat_universe=True,
        n=0.968,
        omega_suppress=False,
        suppress_rad=False,
        pk_norm=0.8,
    )

    eta = cosmo.background.eta(a=0.4)
    eta2 = cosmo.background.eta(a=[0.4, 0.5])  # ,dist=True)
    assert relative_differences(eta, 6664.182275749022) <= limit1
    assert np.isclose(eta, eta2[0], atol=0, rtol=1e-8)


def test_chi_flatDM(cosmo, data):
    """
    The following test compares the analytic solutions with the PyCosmo predictions
    for a flat DM-dominated Universe
    """

    hvalues = np.arange(0.4, 0.9, 0.1)
    z = data[1:, 1]
    chi_analitic = (2 * 1.0) * (1 - 1 / (np.sqrt(1 + z)))
    R0_values = [7494.8114, 5995.8492, 4996.5410, 4282.7494, 3747.4057]

    for k in range(len(hvalues)):
        cosmo.set(h=hvalues[k])
        cosmo.set(omega_m=1.0, omega_l=0.0, flat_universe=False)
        chi = cosmo.background.dist_rad_a(a=data[1:, 0])
        chi_value = chi_analitic * R0_values[k]
        assert (relative_differences(chi, chi_value) <= limit2).all()


def test_omega_a(cosmo):
    """
    Test Cosmo.Background.omega_k_a, which calculates the curvature for a given scale
    factor input: a - scale factor [no dimensions] output: [no dimensions]
    """

    # Case with omega_r > 0
    bg = cosmo.background
    assert relative_differences(bg._omega_a(a=1), 1.0) == 0.0
    assert bg._omega_a(a=1) == 1.0
    assert bg._omega_m_a(a=1) + bg._omega_l_a(a=1) + bg._omega_r_a(a=1) == 1.0

    # Case with omega_r = 0
    cosmo.set(omega_suppress=True)
    assert bg._omega_r_a(a=1) == 0.0
    assert bg._omega_a(a=1) == bg._omega_m_a(a=1) + bg._omega_l_a(a=1)


def test_omega_k_a(background):
    assert (1.0 - background._omega_a(a=1)) == 0.0
    assert (background._omega_k_a(a=1) - background._omega_a(a=1)) == -1.0


def test_pickling(background):
    import pickle

    bg_turnaround = pickle.loads(pickle.dumps(background))
    assert background.__dict__.keys() == bg_turnaround.__dict__.keys()
    # checking values here fails because nbo object holds many objects
    # which can not be compared.


def test_rpbh_a_for_regression(cosmo):
    # Compared numerical value computed with CCL
    cosmo.set(
        h=0.67,
        omega_m=0.3,
        omega_b=0.03,
        flat_universe=True,
        n=0.968,
        omega_suppress=False,
        suppress_rad=False,
        pk_norm=0.8,
    )

    assert abs(cosmo.background._r_bph_a(1.0) - 408.738872507) < 2.05e-5
    assert abs(cosmo.background._r_bph_a(0.5) - 204.369436253) < 1.05e-5
    # assert abs(background._r_bph_a(1.0) - 669.50480159836) < 1e-8
    # assert abs(background._r_bph_a(0.5) - 334.75240079918) < 1e-8


def test_cs_approx_for_regression(cosmo):
    # Compared numerical value computed with CCL
    cosmo.set(
        h=0.67,
        omega_m=0.3,
        omega_b=0.03,
        flat_universe=True,
        n=0.968,
        omega_suppress=False,
        suppress_rad=False,
        pk_norm=0.8,
    )

    assert abs(cosmo.background._cs_approx(1.0) - 0.0285223817724) < 7.05e-10
    assert abs(cosmo.background._cs_approx(0.5) - 0.0402876065544) < 1e-9
    # assert abs(background._cs_approx(1.0) - 0.022296588901102962) < 1e-8
    # assert abs(background._cs_approx(0.5) - 0.031508650956966464) < 1e-8


def test_chi(background):
    c0 = background._chi(0.5)
    assert abs(c0 - 0.010909022244375913) < 1e-8


def test_visibility_function(background):
    assert abs(background.g_a(0.001) - 1.35888e-02) < 1e-7


def test_eta_to_a(background):
    a = np.logspace(-10, 0, 10)
    eta = background.eta(a)
    assert np.allclose(a, background.eta_to_a(eta), atol=0.0, rtol=2e-7)


if __name__ == "__main__":
    import pytest

    pytest.main(["tests/test_background.py::test_transverse_comoving_distance"])
