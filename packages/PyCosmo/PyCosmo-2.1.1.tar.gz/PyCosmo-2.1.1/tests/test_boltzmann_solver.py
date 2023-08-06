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

import csv
import os
import sys

import numpy as np
import pytest
import scipy.interpolate

from PyCosmo import build

HERE = os.path.dirname(os.path.abspath(__file__))

np.set_printoptions(precision=9)


def allclose(x, y, *a, **kw):
    ok = np.allclose(x, y, *a, **kw)
    if not ok:
        rel_err = np.max(np.abs(x / y - 1.0))
        abs_err = np.max(np.abs(x - y))
        print(f"max rel err: {rel_err}, max abs err: {abs_err}", file=sys.stderr)
    return ok


def _setup_cosmo(model, **kw):

    c = build(model, **kw)
    c.set(
        pk_type="boltz",
        pk_nonlin_type=None,
        initial_conditions="class",
        recomb="class",
        recomb_dir=os.path.join(HERE, "comparison_files/class_comparison"),
        recomb_filename="test_thermodynamics.dat",
        table_size=5000,
        pk_norm_type="deltah",
        pk_norm=4.809098157516671e-05,
        N_massless_nu=3.0,
        boltzmann_rtol=1e-6,
        boltzmann_atol=1e-8,
        boltzmann_h0=1e-8,
        n_cores=1,
    )

    return c


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_slow():
    return _setup_cosmo("lcdm", l_max=50)


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_slow_sigma8():
    c = _setup_cosmo("lcdm", l_max=50)
    c.set(pk_norm_type="sigma8", boltzmann_h0=0.0)
    return c


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_slow_lcdm_rsa():
    return _setup_cosmo("lcdm", rsa=True, l_max=50)


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_5():
    return _setup_cosmo("lcdm", l_max=5)


@pytest.fixture(scope="module")
def cosmo_fast():
    return _setup_cosmo("lcdm", l_max=3)


@pytest.fixture(scope="module")
def cosmo_fast_A_s():
    c = _setup_cosmo("lcdm", l_max=3)
    c.set(pk_norm_type="A_s", n_cores=1)
    return c


@pytest.mark.slow
@pytest.fixture(scope="module")
def cosmo_fast_lcdm_rsa():
    return _setup_cosmo("lcdm", rsa=True, l_max=3)


@pytest.fixture(scope="module")
def cosmo_fast_wcdm():
    return _setup_cosmo("wcdm", l_max=3)


@pytest.fixture(scope="module")
def cosmo_fast_wcdm_rsa():
    return _setup_cosmo("wcdm", l_max=3, rsa=True)


@pytest.mark.parametrize(
    "index,rtol,lasti",
    [
        (0, 5.5e-6, 140),
        (1, 3.2e-7, 270),
        (2, 7e-6, 540),
        (3, 3e-5, 740),
        (4, 2e-4, 1320),
    ],
)
@pytest.mark.slow
def test_class_comparison(cosmo_slow, index, rtol, lasti):
    ref = _read_class_data(cosmo_slow, index)

    fields = cosmo_slow.lin_pert.fields(k=ref["k"], grid=np.log(ref["a"]), sec_factor=3)

    # tests if grid is matched
    assert allclose(fields.a, ref["a"], rtol=1e-12, atol=0.0)

    assert allclose(fields.Phi[-lasti:], ref["Phi"][-lasti:], rtol=rtol, atol=0.0)
    assert allclose(fields.delta[-lasti:], ref["delta"][-lasti:], rtol=rtol, atol=0.0)
    assert allclose(
        fields.delta_b[-lasti:], ref["delta_b"][-lasti:], rtol=rtol, atol=0.0
    )
    assert allclose(fields.u_b[-lasti:], ref["u_b"][-lasti:], rtol=rtol, atol=0.0)
    assert allclose(fields.u[-lasti:], ref["u"][-lasti:], rtol=rtol, atol=0.0)


@pytest.mark.skip
def test_for_regression(cosmo_fast, regtest, runs_on_ci_server):

    regtest.identifier = "ci" if runs_on_ci_server else "dev"

    fields = cosmo_fast.lin_pert.fields(k=0.2, grid=np.array((-16, -2, -1, 0)))

    for field in [
        "delta",
        "delta_b",
        "econ",
        "lna",
        "Phi",
        "Theta",
        "Theta_P",
        "u",
        "u_b",
    ]:
        values = np.array(getattr(fields, field))  # remove lna_0 from solver
        for i, row in enumerate(values):
            for j, v in enumerate(row.flatten()):
                print(
                    "{0:<8s} {1:2d} {2:2d} {3:+.6e}".format(field, i, j, v),
                    file=regtest,
                )


@pytest.mark.slow
def test_growth_with_now(cosmo_slow):
    a = [0.01, 0.1, 0.5, 0.7, 1.0]
    growth = cosmo_slow.lin_pert.growth_a(k=1.0, a=a)

    assert len(growth) == 5
    # check that the growth factor should be normalised to 1 at a=1.
    assert growth[-1] == 1.0
    # check growth factor for different values of a
    assert allclose(
        growth, [0.01387422, 0.12933645, 0.61223286, 0.80168374, 1.0], rtol=1e-4, atol=0
    )


def test_growth_with_now_fast(cosmo_fast):
    a = [0.01, 0.1, 0.5, 0.7, 1.0]
    growth = cosmo_fast.lin_pert.growth_a(k=1.0, a=a)

    assert len(growth) == 5
    # check that the growth factor should be normalised to 1 at a=1.
    assert growth[-1] == 1.0
    # check growth factor for different values of a
    assert allclose(
        growth, [0.01387416, 0.12933634, 0.61223281, 0.80168371, 1.0], atol=0
    )
    # TODO: perhaps compare to growth factor from approx


@pytest.mark.slow
def test_growth_without_now(cosmo_slow):
    a = [0.1, 0.5]
    growth = cosmo_slow.lin_pert.growth_a(k=1.0, a=a)

    # check growth factor for different values of a
    assert allclose(growth, [0.12933645, 0.61223286], atol=0)


def test_growth_without_now_fast(cosmo_fast):
    a = [0.1, 0.5]
    growth = cosmo_fast.lin_pert.growth_a(k=1.0, a=a)

    # check growth factor for different values of a
    assert allclose(growth, [0.12933673, 0.61223351], atol=0)


@pytest.mark.slow
def test_growth_scalar(cosmo_slow):
    a = 0.1
    growth = cosmo_slow.lin_pert.growth_a(k=1.0, a=a)

    print(growth)

    assert np.isscalar(growth)
    # check growth factor for different values of a
    assert allclose([growth], [0.1293364498646445], atol=0)


def test_growth_scalar_fast(cosmo_fast):
    a = 0.1
    growth = cosmo_fast.lin_pert.growth_a(k=1.0, a=a)

    print(growth)

    assert np.isscalar(growth)
    # check growth factor for different values of a
    assert allclose([growth], [0.12933633766941074], atol=0)


@pytest.mark.slow
def test_transfer_boltzmann(cosmo_slow):
    k = [1e-3, 1e-2, 1e-1, 1e0, 1e1]  # wave number [Mpc^-1]

    transfer = cosmo_slow.lin_pert.transfer_k(k)  # , atol=1e-4, rtol=1e-4)
    assert allclose(
        transfer,
        np.array(
            [
                9.89150606e-01,
                6.95568675e-01,
                8.09044296e-02,
                2.36268308e-03,
                4.20831199e-05,
            ]
        ),
        atol=0,
    )


def test_transfer_boltzmann_fast(cosmo_fast):
    k = [1e-3, 1e-1]  # wave number [Mpc^-1]
    transfer = cosmo_fast.lin_pert.transfer_k(k)
    assert allclose(transfer, np.array([0.98914376, 0.07992963]), atol=0)


def test_powerspec_boltzmann(cosmo_slow):
    k = [1e-3, 1e-2, 1e-1, 1e0, 1e1]  # wave number [Mpc^-1]

    powerspec_z0 = cosmo_slow.lin_pert.powerspec_a_k(1.0, k)[:, 0]  # z=0
    powerspec_z1 = cosmo_slow.lin_pert.powerspec_a_k(0.5, k)[:, 0]  # z=1

    print(powerspec_z0)
    print(
        powerspec_z0
        - np.array(
            [
                1.50269538e04,
                7.43153304e04,
                1.00556208e04,
                8.57651092e01,
                2.71782506e-01,
            ]
        )
    )

    assert allclose(
        powerspec_z0,
        np.array([+1.50267e04, +7.43042e04, +1.00516e04, +8.57420e01, +2.71984e-01]),
        rtol=1e-4,
        atol=1,
    )
    assert allclose(
        powerspec_z1,
        np.array([+5.63246e03, +2.78515e04, +3.76764e03, +3.21387e01, +1.01948e-01]),
        rtol=1e-4,
        atol=1,
    )


def test_powerspec_boltzmann_sigma8(cosmo_slow_sigma8):

    k = [1e-3, 1e-2, 1e-1, 1e0, 1e1]  # wave number [Mpc^-1]

    powerspec_z0 = cosmo_slow_sigma8.lin_pert.powerspec_a_k(1.0, k)[:, 0]  # z=0
    powerspec_z1 = cosmo_slow_sigma8.lin_pert.powerspec_a_k(0.5, k)[:, 0]  # z=1

    assert allclose(
        powerspec_z0,
        np.array(
            [
                5.39427520e-05,
                2.66759816e-04,
                3.60934757e-05,
                3.07821814e-07,
                9.76573166e-10,
            ]
        ),
        atol=0,
    )
    assert allclose(
        powerspec_z1,
        np.array(
            [
                2.01917325e-05,
                9.98655081e-05,
                1.35121495e-05,
                1.15237854e-07,
                3.65597039e-10,
            ]
        ),
        atol=0,
    )


def test_powerspec_boltzmann_fast(cosmo_fast):
    k = [1e-3, 1e-1]  # wave number [Mpc^-1]
    powerspec_z0 = cosmo_fast.lin_pert.powerspec_a_k(1.0, k)[:, 0]  # z=0
    powerspec_z1 = cosmo_fast.lin_pert.powerspec_a_k(0.5, k)[:, 0]  # z=1

    print(powerspec_z0)
    print(powerspec_z1)

    assert allclose(powerspec_z0, [15026.79787619, 9812.12915612], rtol=1e-4, atol=1)
    assert allclose(powerspec_z1, [5632.47978411, 3677.87066588], rtol=1e-4, atol=1)

    powerspec_matrix = cosmo_fast.lin_pert.powerspec_a_k([0.5, 1], k, diag_only=False)
    powerspec_diag = cosmo_fast.lin_pert.powerspec_a_k([0.5, 1], k, diag_only=True)

    diff = np.diag(powerspec_matrix) - powerspec_diag
    assert allclose(np.diag(powerspec_matrix), powerspec_diag), diff


def test_powerspec_boltzmann_fast_A_s_parallel(cosmo_fast_A_s):
    cosmo = cosmo_fast_A_s

    k = [1e-3, 1e-2, 1e-1]  # wave number [Mpc^-1]
    a = [0.1, 1]
    powerspec_serial = cosmo.lin_pert.powerspec_a_k(a, k)
    assert powerspec_serial.shape == (3, 2)

    cosmo.set(n_cores=2)

    powerspec_parallel = cosmo.lin_pert.powerspec_a_k(a, k)
    assert powerspec_parallel.shape == (3, 2)

    assert np.all(powerspec_serial == powerspec_parallel)


def test_powerspec_boltzmann_fast_A_s(cosmo_fast_A_s):
    cosmo = cosmo_fast_A_s

    k = [1e-3, 1e-1]  # wave number [Mpc^-1]
    powerspec_0 = cosmo.lin_pert.powerspec_a_k(1.0, k)
    assert powerspec_0.shape == (2, 1)

    powerspec_1 = cosmo.lin_pert.powerspec_a_k([0.5, 0.6, 1.0], k)
    assert powerspec_1.shape == (2, 3)

    powerspec_2 = cosmo.lin_pert.powerspec_a_k([0.5, 0.6], k, diag_only=True)
    assert powerspec_2.shape == (2,)

    powerspec_3 = cosmo.lin_pert.powerspec_a_k([0.5, 0.6], k, diag_only=False)
    assert powerspec_3.shape == (2, 2)
    assert np.allclose(np.diag(powerspec_3), powerspec_2, atol=0, rtol=1e-8)

    p0 = cosmo.lin_pert.powerspec_a_k(0.5, k).flatten()
    assert np.allclose(p0, powerspec_3[:, 0], atol=0, rtol=1e-8)

    p0 = cosmo.lin_pert.powerspec_a_k(0.6, k).flatten()
    assert np.allclose(p0, powerspec_3[:, 1], atol=0, rtol=1e-8)

    p0 = cosmo.lin_pert.powerspec_a_k([0.5, 0.6], k[0]).flatten()
    assert np.allclose(p0, powerspec_3[0, :], atol=0, rtol=1e-8)

    p0 = cosmo.lin_pert.powerspec_a_k([0.5, 0.6], k[1]).flatten()
    assert np.allclose(p0, powerspec_3[1, :], atol=0, rtol=1e-8)

    p0 = cosmo.lin_pert.powerspec_cb_a_k([0.5, 0.6], k[1]).flatten()
    assert allclose(p0, np.array([8.11634271e07, 1.10089934e08]), atol=0)


@pytest.mark.skip
@pytest.mark.slow
def test_native_vs_compiled(cosmo_slow):
    """
    TODO: refactor this to a method in LinearPertubation.py so we can compare
    solves next to each other.
    """

    cosmo = cosmo_slow

    k = 0.1

    fields_native = cosmo.lin_pert.fields(k=k, verbose=True)
    fields_py = cosmo.lin_pert.fields_py(k=k, verbose=True)
    max_err = _max_err(fields_native, fields_py)
    assert max_err < 0.00018  # max value determined on linux


def _max_err(fields_native, fields_py):

    n_native = int(fields_native._ptr[0])
    n_python = int(fields_py._ptr[0])

    lna_native = np.array(fields_native._lna[:n_native])
    lna_python = np.array(fields_py._lna[:n_python])

    y_native = fields_native._y[:n_native, :]
    y_python = fields_py._y[:n_python, :]

    n_fields = y_native.shape[1]
    rel_errs = []
    for c in range(n_fields):
        ip = scipy.interpolate.interp1d(lna_native, y_native[:, c], "cubic")
        y_tobe = ip(lna_python)
        y_is = y_python[:, c]
        # max deviation corrected by scale:
        diff = np.max((y_is - y_tobe) / np.max(np.abs(y_tobe)))
        rel_errs.append(diff)

    return max(rel_errs)


@pytest.mark.skip
def test_native_vs_compiled_fast(cosmo_fast):
    """
    TODO: refactor this to a method in LinearPertubation.py so we can compare
    solves next to each other.
    """

    cosmo = cosmo_fast

    k = 0.1

    fields_native = cosmo.lin_pert.fields(k=k, verbose=True)
    fields_py = cosmo.lin_pert.fields_py(k=k, verbose=True)
    max_err = _max_err(fields_native, fields_py)
    assert max_err < 2e-12  # max value determined on linux


def _read_class_data(cosmo, index):

    # get cosmo parameters
    h = cosmo.params.h
    H_0 = 1 / cosmo.params.rh
    Omega_k = cosmo.params.omega_k
    Omega_r = cosmo.params.omega_r
    Omega_m = cosmo.params.omega_m
    Omega_gamma = cosmo.params.omega_gamma
    Omega_nu = cosmo.params.omega_neu
    Omega_l = cosmo.params.omega_l
    Omega_b = cosmo.params.omega_b
    Omega_dm = cosmo.params.omega_dm

    # load class data
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "./comparison_files/class_comparison/test_perturbations_k{0}_s.dat".format(
                index
            ),
        ),
        "rt",
    ) as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        rows = [list(filter(None, row)) for row in reader]
    data = np.array([[float(x) for x in row] for row in rows[2:]])
    k = float(rows[0][6])

    # cleanup the grid
    limit = 1e-4
    filt = np.empty(data[:, 1].shape, dtype=bool)
    lna0 = np.log(data[0, 1])
    for idx, lna in enumerate(np.log(data[:, 1])):
        if idx > 0 and lna - lna0 < limit:
            filt[idx] = False
        else:
            filt[idx] = True
            lna0 = lna

    # extract class fields
    fields = dict(
        {
            "a": data[:, 1][filt],
            "theta_0": (data[:, 2] / 4.0)[filt],
            "theta_1": (data[:, 3] / (3 * k))[filt],
            "theta_2": (data[:, 4] / 2.0)[filt],
            "delta_b": data[:, 8][filt],
            "u_b": (data[:, 9] / k)[filt],
            "Phi": -data[:, 11][filt],
            "N0": (data[:, 12] / 4.0)[filt],
            "N1": (data[:, 13] / (3.0 * k))[filt],
            "N2": (data[:, 14] / 2.0)[filt],
            "delta": data[:, 15][filt],
            "u": (data[:, 16] / k)[filt],
        }
    )

    fields["H"] = H_0 * (
        Omega_r * 1.0 / fields["a"] ** 4
        + Omega_m * 1.0 / fields["a"] ** 3
        + Omega_k * 1.0 / fields["a"] ** 2
        + Omega_l
    ) ** (1.0 / 2.0)
    fields["k"] = k / h
    fields["econ"] = (
        (-2.0 / 3.0 * (fields["k"] / (fields["a"] * H_0)) ** 2 * fields["Phi"])
        + (
            (Omega_dm * fields["delta"] + Omega_b * fields["delta_b"])
            / fields["a"] ** 3
            + 4.0
            * (Omega_gamma * fields["theta_0"] + Omega_nu * fields["N0"])
            / fields["a"] ** 4
        )
        + 3.0
        * fields["a"]
        * fields["H"]
        / fields["k"]
        * (
            (Omega_dm * fields["u"] + Omega_b * fields["u_b"]) / fields["a"] ** 3
            + 4.0
            * (Omega_gamma * fields["theta_1"] + Omega_nu * fields["N1"])
            / fields["a"] ** 4
        )
    ) / (
        (Omega_dm + Omega_b) / fields["a"] ** 3
        + (Omega_gamma + Omega_nu) / fields["a"] ** 4
    )

    return fields


@pytest.mark.skip
def test_odeint_vs_native(cosmo_5, tmpdir, runs_on_ci_server):

    k = 0.1
    l_max = 5

    (
        max_econ_odeint,
        errs,
        rel_errs,
    ) = cosmo_5.lin_pert.compare_fields_odeint_vs_native(
        k=k,
        l_max=l_max,
        verbose=True,
        plot_folder=tmpdir.strpath,
        h0=0,
        wrappers_folder=tmpdir.strpath,
    )

    assert max_econ_odeint < 3e-4

    errs_tobe = np.array(
        [
            1.27445063e-05,
            1.91713912e00,
            3.33263994e-03,
            1.97937674e00,
            3.33479473e-03,
            1.75583315e-02,
            1.38397922e-03,
            4.98452108e-03,
            1.37321625e-02,
            5.67477116e-04,
            3.26659786e-03,
            8.43649301e-03,
            5.27186251e-04,
            3.07817557e-03,
            4.50714046e-03,
            4.52985041e-04,
            2.64412533e-03,
            7.79051468e-03,
            2.31176643e-04,
            2.89158861e-03,
            9.08209093e-03,
            4.90029964e-04,
            3.04384901e-03,
        ]
    )

    if runs_on_ci_server:
        errs_tobe = np.array(
            [
                +1.48076e-05,
                +1.91662e00,
                +3.33171e-03,
                +1.97890e00,
                +3.33387e-03,
                +1.75083e-02,
                +1.37579e-03,
                +4.99722e-03,
                +1.36981e-02,
                +5.65416e-04,
                +3.27902e-03,
                +8.42188e-03,
                +5.26579e-04,
                +3.08841e-03,
                +4.50174e-03,
                +4.56788e-04,
                +2.64807e-03,
                +7.74884e-03,
                +2.30495e-04,
                +2.88218e-03,
                +9.04632e-03,
                +4.93286e-04,
                +3.05537e-03,
            ]
        )

    assert np.all(errs <= 1.1 * errs_tobe)

    rel_errs_tobe = np.array(
        [
            +1.78388e-04,
            +1.75684e-04,
            +1.77895e-04,
            +2.37879e-02,
            +8.38733e00,
            +2.12199e01,
            +1.80918e02,
            +1.48073e00,
            +2.01919e03,
            +2.72293e02,
            +1.64658e03,
            +1.73592e03,
            +2.00220e02,
            +1.58298e02,
            +4.62604e03,
            +1.07712e02,
            +6.74283e02,
            +6.22117e02,
            +7.32178e02,
            +3.14432e03,
            +6.76781e02,
            +2.43766e02,
            +1.96230e02,
        ]
    )

    if runs_on_ci_server:
        rel_errs_tobe = np.array(
            [
                +1.78324e-04,
                +1.75618e-04,
                +1.77831e-04,
                +2.37915e-02,
                +8.39032e00,
                +2.12176e01,
                +1.80915e02,
                +1.48111e00,
                +2.01898e03,
                +1.65571e03,
                +1.64608e03,
                +1.73591e03,
                +2.02932e02,
                +1.63570e02,
                +1.20676e03,
                +2.35455e02,
                +4.07980e02,
                +3.31303e03,
                +7.32150e02,
                +6.35598e03,
                +1.78004e04,
                +2.09015e02,
                +2.48593e02,
            ]
        )

    assert np.all(rel_errs <= 1.1 * rel_errs_tobe)


def test_powerspec_fast_api(cosmo_fast):
    ps1 = cosmo_fast.lin_pert.powerspec_a_k(a=0.5, k=0.5)[0, 0]
    ps2 = cosmo_fast.lin_pert.powerspec_a_k(a=0.6, k=0.5)[0, 0]
    ps3 = cosmo_fast.lin_pert.powerspec_a_k(a=0.5, k=0.9)[0, 0]
    ps4 = cosmo_fast.lin_pert.powerspec_a_k(a=0.6, k=0.9)[0, 0]

    ps_matrix = cosmo_fast.lin_pert.powerspec_a_k(a=[0.5, 0.6], k=[0.5, 0.9])
    assert allclose(ps_matrix, np.array([[ps1, ps2], [ps3, ps4]]))


def test_powerspec_parallel(cosmo_fast):

    # inverse order to check reodering in parallel version:
    kvec = 10 ** np.linspace(-5, -1, 7)[::-1]

    ps_serial = cosmo_fast.lin_pert.powerspec_a_k(0.5, kvec)

    cosmo_fast.set(n_cores=2)
    ps_parallel = cosmo_fast.lin_pert.powerspec_a_k(0.5, kvec)

    assert np.all(ps_serial == ps_parallel)


def test_transfer_parallel(cosmo_fast):
    k = 10 ** np.linspace(-3, 0, 10)
    transfer_sequential = cosmo_fast.lin_pert.transfer_k(k)

    cosmo_fast.set(n_cores=2)
    transfer_parallel = cosmo_fast.lin_pert.transfer_k(k)
    assert np.all(transfer_parallel == transfer_sequential)


def test_boltzmann_lcdm_rsa_fast(cosmo_fast_lcdm_rsa):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_fast_lcdm_rsa.lin_pert.fields(grid=[-5], k=0.1)

    fields_to_be = np.array(
        [
            [-7.20394e-02],
            [-1.07712e02],
            [+2.18597e00],
            [-5.45466e01],
            [+1.94219e00],
            [-7.21120e-02],
            [+0.00000e00],
            [-7.20394e-02],
            [-9.60803e-05],
            [+0.00000e00],
            [-9.71249e-05],
            [+0.00000e00],
            [+0.00000e00],
            [+0.00000e00],
            [+0.00000e00],
            [+0.00000e00],
            [+0.00000e00],
            [-9.30424e01],
        ]
    )
    # without econ or more:
    assert allclose(fields._y[:18], fields_to_be, atol=0, rtol=2e-4), (
        fields._y[:18] / fields_to_be - 1.0
    )
    assert allclose(fields._y[:8], fields_to_be[:8], atol=0), (
        fields._y[:8] / fields_to_be[:8] - 1.0
    )


def test_boltzmann_wcdm_fast(cosmo_fast_wcdm, runs_on_ci_server):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_fast_wcdm.lin_pert.fields(grid=[-5], k=0.01)

    fields_to_be = np.array(
        [
            [-4.81150e-01],
            [-7.42867e00],
            [+1.44111e00],
            [-7.15135e00],
            [+1.42331e00],
            [-3.62890e-02],
            [+4.77900e-01],
            [-4.39656e-01],
            [-8.02904e-04],
            [-4.39100e-01],
            [-9.06699e-02],
            [+5.60059e-04],
            [-3.61184e-02],
            [-9.48046e-02],
            [+4.65046e-04],
            [-5.86741e-02],
            [-9.44822e-02],
            [+1.39874e-03],
        ]
    )

    assert allclose(
        fields._y[:18],
        fields_to_be,
        atol=0,
        rtol=8e-6 if runs_on_ci_server else 5e-6,
    ), np.abs(fields._y[:18] / fields_to_be[:18] - 1.0)


def test_boltzmann_wcdm_fast_rsa(cosmo_fast_wcdm_rsa, runs_on_ci_server):

    # avoid oscillations which differ on different platforms:
    fields = cosmo_fast_wcdm_rsa.lin_pert.fields(grid=[-5], k=0.01)

    fields_to_be = np.array(
        [
            [-4.811504459e-01],
            [-7.428673029e00],
            [1.441112820e00],
            [-7.151349160e00],
            [1.423310137e00],
            [-3.628895498e-02],
            [4.778997459e-01],
            [-4.396557915e-01],
            [-8.029039260e-04],
            [-4.391003531e-01],
            [-9.066994306e-02],
            [5.600589322e-04],
            [-3.611841795e-02],
            [-9.480457271e-02],
            [4.650456219e-04],
            [-5.867414394e-02],
            [-9.448215926e-02],
            [1.398739695e-03],
        ]
    )

    assert allclose(
        fields._y[:18],
        fields_to_be,
        atol=0,
        rtol=8e-6 if runs_on_ci_server else 2e-6,
    ), np.abs(fields._y[:18] / fields_to_be - 1.0)


@pytest.mark.slow
def test_boltzmann_lcdm_rsa(cosmo_slow, cosmo_slow_lcdm_rsa):
    kvec = np.linspace(1e-4, 1, 50)

    ps = cosmo_slow.lin_pert.powerspec_a_k(a=[0.5, 0.9, 1], k=kvec)
    ps_rsa = cosmo_slow_lcdm_rsa.lin_pert.powerspec_a_k(a=[0.5, 0.9, 1], k=kvec)

    assert allclose(ps, ps_rsa, rtol=8e-4, atol=0)
